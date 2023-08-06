import io
import logging
import os
import struct
import tempfile
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime
from typing import List, Union

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

V8_FILE_HEADER_NAME = "FileHeader"
V8_FILE_HEADER_SIZE = 16
V8_FILE_HEADER_FORMAT = "iiii"

V8_ELEM_HEADER_SIZE = 20
V8_ELEM_HEADER_FORMAT = "QQi"

V8_ELEM_OFFSET_SIZE = 12
V8_ELEM_OFFSET_FORMAT = "iii"

V8_BLOCK_HEADER_SIZE = 31
V8_BLOCK_HEADER_FORMAT = "cc8sc8sc8sccc"

V8_DEFAULT_PAGE_SIZE = 512
V8_FF_SIGNATURE = 0x7FFFFFFF


@dataclass(frozen=True)
class FileHeader:
    next_page_addr: int
    page_size: int
    storage_ver: int
    reserved: int

    def pack(self) -> bytes:
        return struct.pack(
            V8_FILE_HEADER_FORMAT,
            self.next_page_addr,
            self.page_size,
            self.storage_ver,
            self.reserved,
        )


@dataclass(frozen=True)
class ElemHeader:
    date_creation: int
    date_modification: int
    reserved: int
    name_data: bytes = b""

    def pack(self) -> bytes:
        return (
            struct.pack(
                V8_ELEM_HEADER_FORMAT,
                self.date_creation,
                self.date_modification,
                self.reserved,
            )
            + self.name_data
        )

    def get_name(self) -> str:
        name = bytearray(self.name_data).decode()
        return name.replace("\x00", "")


@dataclass(frozen=True)
class ElemOffset:
    elem_header_offset: int
    elem_data_offset: int
    next: int

    def pack(self) -> bytes:
        return struct.pack(
            V8_ELEM_OFFSET_FORMAT,
            self.elem_header_offset,
            self.elem_data_offset,
            self.next,
        )


@dataclass(frozen=True)
class BlockHeader:
    EOL_0D: bytes
    EOL_0A: bytes
    data_size_hex: bytes
    space1: bytes
    page_size_hex: bytes
    space2: bytes
    next_page_addr_hex: bytes
    space3: bytes
    EOL2_0D: bytes
    EOL2_0A: bytes

    def data_size(self):
        return int(self.data_size_hex, 16)

    def page_size(self):
        return int(self.page_size_hex, 16)

    def next_page(self):
        return int(self.next_page_addr_hex, 16)

    def pack(self) -> bytes:
        return struct.pack(
            V8_BLOCK_HEADER_FORMAT,
            self.EOL_0D,
            self.EOL_0A,
            self.data_size_hex,
            self.space1,
            self.page_size_hex,
            self.space2,
            self.next_page_addr_hex,
            self.space3,
            self.EOL2_0D,
            self.EOL2_0A,
        )


@dataclass(frozen=True)
class BlockData:
    data: bytes
    size: int


@dataclass
class V8BlockMetadata:

    header: Union[BlockHeader, None]
    data: Union[BlockData, None]

    def get_data(self, offset: int = None, size: int = None) -> bytes:
        # пустой блок, параметры игнорируются
        if self.data is None:
            return bytearray()
        else:
            block: BlockData = self.data
        # заполненный блок
        if size is None and offset is None:
            return block.data
        elif size is None:
            return block.data[offset:]
        elif offset is None:
            return block.data[0:size]
        else:
            offset_size = offset + size
            return block.data[offset:offset_size]

    def get_size(self) -> int:
        if self.data is None:
            return 0
        return self.data.size

    def pack(self) -> bytes:
        if self.header is None or self.data is None:
            raise ValueError("metadata block is empty")
        return self.header.pack() + self.data.data


@dataclass
class V8ElementMetadata:

    offset: ElemOffset
    header_meta: V8BlockMetadata
    header: ElemHeader
    meta: V8BlockMetadata

    def get_name(self) -> str:
        return self.header.get_name()


@dataclass
class V8ElementsMetadata:

    meta: V8BlockMetadata
    entities: List[V8ElementMetadata]


@dataclass
class V8FileMetadata:

    header: FileHeader
    elements: V8ElementsMetadata


@dataclass(frozen=True)
class V8ElementParts:
    name: str
    data: str
    header: str

    def header_size(self):
        """
        Размер заголовка в байтах
        """
        # Результат можно сверить с фактическим self.header
        return V8_ELEM_HEADER_SIZE + (len(self.name) * 2) + 4

    def data_size(self):
        return os.path.getsize(self.data)


@dataclass
class V8FileParts:

    header: str
    elements: List[V8ElementParts]


def _parse_elements(buffer) -> V8ElementsMetadata:
    meta = _parse_block(buffer)
    count = int(meta.get_size() / V8_ELEM_OFFSET_SIZE)
    entities = []
    for i in range(count):
        offset_data = meta.get_data(
            i * V8_ELEM_OFFSET_SIZE, (i + 1) * V8_ELEM_OFFSET_SIZE
        )
        offset = ElemOffset(*struct.unpack(V8_ELEM_OFFSET_FORMAT, offset_data))
        element = _parse_element(buffer, offset)
        entities.append(element)
    return V8ElementsMetadata(meta=meta, entities=entities)


def _parse_block(buffer) -> V8BlockMetadata:
    header_struct = struct.unpack(
        V8_BLOCK_HEADER_FORMAT, buffer.read(V8_BLOCK_HEADER_SIZE)
    )
    header = BlockHeader(*header_struct)
    data = _read_block_data(buffer, header)
    return V8BlockMetadata(header, data)


def _parse_element(buffer, offset) -> V8ElementMetadata:

    if offset.next != V8_FF_SIGNATURE:
        raise NotImplementedError
    buffer.seek(offset.elem_header_offset, 0)

    header_meta = _parse_block(buffer)
    header_struct = struct.unpack(
        V8_ELEM_HEADER_FORMAT, header_meta.get_data(size=V8_ELEM_HEADER_SIZE)
    ) + (header_meta.get_data(offset=V8_ELEM_HEADER_SIZE),)
    header = ElemHeader(*header_struct)

    if offset.elem_data_offset != V8_FF_SIGNATURE:
        buffer.seek(offset.elem_data_offset, 0)
        meta = _parse_block(buffer)
    else:
        meta = V8BlockMetadata(None, None)

    return V8ElementMetadata(
        header_meta=header_meta, offset=offset, header=header, meta=meta
    )


def _read_block_data(buffer, header: BlockHeader) -> BlockData:

    data = bytes()
    page = header
    read_in_bytes = 0
    while read_in_bytes < header.data_size():

        bytes_to_read = min(page.page_size(), header.data_size() - read_in_bytes)
        read_in_bytes += bytes_to_read

        data += buffer.read(bytes_to_read)
        if page.next_page() != V8_FF_SIGNATURE:
            buffer.seek(page.next_page(), 0)
            header_struct = struct.unpack(
                V8_BLOCK_HEADER_FORMAT, buffer.read(V8_BLOCK_HEADER_SIZE)
            )
            page = BlockHeader(*header_struct)
        else:
            break

    return BlockData(data, header.data_size())


def _find_parts(src_dir) -> V8FileParts:
    """Ищет части для сборки .bin"""
    # Заголовок
    header = os.path.join(src_dir, V8_FILE_HEADER_NAME)
    if not os.path.exists(header):
        raise FileNotFoundError(header)
    # Элементы
    elements = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".data"):
                elem_data = os.path.join(root, file)
                elem_header = os.path.join(root, file.replace(".data", ".header"))
                elem_name = file.replace(".data", "")
                if not os.path.exists(elem_header):
                    raise FileNotFoundError(elem_header)
                elem = V8ElementParts(
                    name=elem_name, data=elem_data, header=elem_header
                )
                elements.append(elem)
    return V8FileParts(header=header, elements=elements)


def _build_block_header(size: int) -> BlockHeader:

    # размер страницы

    if size > V8_DEFAULT_PAGE_SIZE:
        page_size = size
    else:
        page_size = V8_DEFAULT_PAGE_SIZE

    # hex

    data_size_hex = str.encode(size.to_bytes(length=4, byteorder="big").hex())
    page_size_hex = str.encode(page_size.to_bytes(length=4, byteorder="big").hex())

    block_header = BlockHeader(
        EOL_0D=b"\r",
        EOL_0A=b"\n",
        data_size_hex=data_size_hex,
        space1=b" ",
        page_size_hex=page_size_hex,
        space2=b" ",
        next_page_addr_hex=b"7fffffff",
        space3=b" ",
        EOL2_0D=b"\r",
        EOL2_0A=b"\n",
    )
    return block_header


def _build_file_header() -> FileHeader:
    return FileHeader(
        next_page_addr=V8_FF_SIGNATURE,
        page_size=V8_DEFAULT_PAGE_SIZE,
        storage_ver=2,
        reserved=0,
    )


def _elem_block_data_size(header_size: int, data_size: int) -> int:
    """
    Расчетный размер элемента
    """
    return _block_data_size(header_size, header_size) + _block_data_size(
        data_size, V8_DEFAULT_PAGE_SIZE
    )


def _block_data_size(data_size: int, page_size: int) -> int:
    return max(page_size, data_size)


def _write_data_block(buffer, data, data_size: int, page_size: int = 0) -> None:

    # размер страницы

    if page_size < data_size:
        page_size = data_size

    # hex

    data_size_hex = str.encode(data_size.to_bytes(length=4, byteorder="big").hex())
    page_size_hex = str.encode(page_size.to_bytes(length=4, byteorder="big").hex())

    block_header = BlockHeader(
        EOL_0D=b"\r",
        EOL_0A=b"\n",
        data_size_hex=data_size_hex,
        space1=b" ",
        page_size_hex=page_size_hex,
        space2=b" ",
        next_page_addr_hex=b"7fffffff",
        space3=b" ",
        EOL2_0D=b"\r",
        EOL2_0A=b"\n",
    )

    buffer.write(block_header.pack())
    if isinstance(data, io.BufferedIOBase):
        buffer.write(data.read())
    else:
        buffer.write(data)

    if page_size > data_size:
        buffer.write(bytes(page_size - data_size))


def _elem_blocks(elements: list) -> list:
    blocks = []
    for elem in elements:
        blocks.append(
            {
                "elem": elem,
                "data_size": elem.header_size(),
                "data_src": elem.header,
                "elem_header": True,
            }
        )
        blocks.append(
            {
                "elem": elem,
                "data_size": elem.data_size(),
                "data_src": elem.data,
                "elem_header": False,
            }
        )
    blocks.sort(key=lambda x: x["data_size"])
    return blocks


def _calc_offsets(elements: list, offset: int = 0) -> OrderedDict:

    blocks = _elem_blocks(elements)

    # Расчет сдвигов

    elements_sorted = []
    elem_map: dict = {x: {} for x in elements}
    for block in blocks:

        elem = block["elem"]
        data_size = block["data_size"]
        if block["elem_header"] is True:
            offset_type = "header_offset"
            page_size = data_size
        else:
            offset_type = "data_offset"
            page_size = V8_DEFAULT_PAGE_SIZE

        if elem not in elements_sorted:
            elements_sorted.append(elem)

        elem_map[elem][offset_type] = offset
        offset += V8_BLOCK_HEADER_SIZE + max(page_size, data_size)

    # Результат

    offsets = OrderedDict(
        [
            (k, ElemOffset(v["header_offset"], v["data_offset"], V8_FF_SIGNATURE,),)
            for k, v in elem_map.items()
        ]
    )

    for key in elements_sorted:
        offsets.move_to_end(key)

    return offsets


def _write_elements(buffer, elements: list) -> None:

    offsets = _write_offset(buffer, elements)
    for element, offset in offsets.items():

        with open(element.header, "r+b") as data:
            buffer.seek(offset.elem_header_offset)
            _write_data_block(buffer, data, element.header_size())

        with open(element.data, "r+b") as data:
            buffer.seek(offset.elem_data_offset)
            _write_data_block(buffer, data, element.data_size(), V8_DEFAULT_PAGE_SIZE)


def _write_offset(buffer, elements) -> OrderedDict:

    offset_data = bytes()
    offset_size = V8_ELEM_OFFSET_SIZE * len(elements)
    offset_elem = (
        buffer.tell() + V8_BLOCK_HEADER_SIZE + max(V8_DEFAULT_PAGE_SIZE, offset_size)
    )

    elements_offsets = _calc_offsets(elements, offset_elem)
    for offset in elements_offsets.values():
        offset_data += offset.pack()

    assert len(offset_data) == offset_size

    _write_data_block(
        buffer, offset_data, data_size=offset_size, page_size=V8_DEFAULT_PAGE_SIZE
    )

    assert buffer.tell() == offset_elem

    return elements_offsets


def _write_header(buffer) -> None:
    header = FileHeader(
        next_page_addr=V8_FF_SIGNATURE,
        page_size=V8_DEFAULT_PAGE_SIZE,
        storage_ver=2,
        reserved=0,
    )
    buffer.write(header.pack())


def _ticks(dt):
    return (dt - datetime(1, 1, 1)).total_seconds() * 10000000


def parse_file(v8file) -> V8FileMetadata:
    """
    Считывает файл в объект модели метаданных
    """
    with open(v8file, "rb") as f:
        header = FileHeader(
            *struct.unpack(V8_FILE_HEADER_FORMAT, f.read(V8_FILE_HEADER_SIZE))
        )
        elements = _parse_elements(f)
        return V8FileMetadata(header=header, elements=elements)


def dump_file(v8file, src_dir) -> None:
    """
    Разбирает файл и записывает части
    """

    file_mdo = parse_file(v8file)

    with open(os.path.join(src_dir, V8_FILE_HEADER_NAME), "w+b") as f:
        f.write(file_mdo.header.pack())

    for elem in file_mdo.elements.entities:
        name = elem.get_name()
        with open(os.path.join(src_dir, f"{name}.header"), "w+b") as f:
            f.write(elem.header.pack())
        with open(os.path.join(src_dir, f"{name}.data"), "w+b") as f:
            f.write(elem.meta.get_data())


def build_file(v8file, src_dir) -> None:
    """
    Собирает файл из частей
    """
    parts = _find_parts(src_dir)
    with open(v8file, mode="w+b", buffering=0) as f:
        _write_header(f)
        _write_elements(f, parts.elements)


def build_form(v8file, module_data, form_data) -> None:
    """
    Собирает Form.bin из данных о элементах и модуле, заголовки генерируются
    """
    with tempfile.TemporaryDirectory() as tmpdir:

        header = os.path.join(tmpdir, "FileHeader")
        module = os.path.join(tmpdir, "module.header")
        form = os.path.join(tmpdir, "form.header")

        # Генерации заголовка файла

        with open(header, mode="w+b", buffering=0) as f:
            _write_header(f)

        # Генерации заголовков элементов (модуль и форма)

        now_ticks = int(_ticks(datetime.utcnow()))

        with open(module, mode="w+b", buffering=0) as f:
            elem_header = ElemHeader(
                date_creation=now_ticks,
                date_modification=now_ticks,
                reserved=0,
                name_data=b"m\x00o\x00d\x00u\x00l\x00e\x00\x00\x00\x00\x00",
            )
            f.write(elem_header.pack())

        with open(form, mode="w+b", buffering=0) as f:
            elem_header = ElemHeader(
                date_creation=now_ticks,
                date_modification=now_ticks,
                reserved=0,
                name_data=b"f\x00o\x00r\x00m\x00\x00\x00\x00\x00",
            )
            f.write(elem_header.pack())

        # Определение структуры
        # TODO нужно сделать апи, которое не зависит от файловой системы

        elements = [
            V8ElementParts(name="form", data=form_data, header=form),
            V8ElementParts(name="module", data=module_data, header=module),
        ]

        parts = V8FileParts(header=header, elements=elements)
        with open(v8file, mode="w+b", buffering=0) as f:
            _write_header(f)
            _write_elements(f, parts.elements)

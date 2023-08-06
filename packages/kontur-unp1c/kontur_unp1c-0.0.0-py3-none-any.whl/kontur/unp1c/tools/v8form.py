import codecs
import uuid
import os
from multiprocessing.dummy import Pool as ThreadPool


class Form:
    """
    Парсер/упорядочиватель формы
    """

    def __init__(self, form_data_path):
        self._form_data_path = form_data_path
        self._form_data_lines = []
        self._form_data_rows = []
        self._form_data_tree = None
        self._form_data_level = 0
        self._all_form_data_array = []

    def _branch(self, parent=None):
        form_data_array = []
        branch = {"rows": form_data_array, "parent": parent}
        self._all_form_data_array.append(form_data_array)
        return branch

    def _read_rows(self, row_number):
        line = self._form_data_lines[row_number]
        line = line.replace("\n", "")
        line = line.replace("\r", "")
        line = line.replace("\t", "")
        if line == "":
            return
        row_data = self._read_line(line)
        self._form_data_rows[row_number] = row_data

    def _read_line(self, line):
        tree = self._branch()
        last_branch = self._form_data_line_to_tree(line, tree)
        row_data = {
            "branch": tree,
            "last_branch": last_branch,
            "open_tag": line[0] == "{",
            "last_property_tag": line[-1] != ",",
        }
        return row_data

    def _form_data_line_to_tree(self, line, tree):
        i = len(line)
        for symbol in reversed(line):
            if symbol == "}":
                new_branch = self._branch(tree)
                new_line_size = i - 1
                new_line = line[0:new_line_size]
                last_branch = self._form_data_line_to_tree(new_line, new_branch)
                self._append_row(tree["rows"], new_branch)
                return last_branch
            elif symbol == "{":
                return tree
            elif symbol == ",":
                tree["rows"].append(None)
            else:
                self._set_row(tree["rows"], symbol)
            i = i - 1
        return tree

    def _append_row(self, rows, row):
        if len(rows) == 0:
            rows.append(row)
        elif rows[-1] is None:
            rows[-1] = row
        else:
            rows.append(row)

    def _set_row(self, rows, value):
        if len(rows) == 0:
            rows.append(value)
        elif rows[-1] is None:
            rows[-1] = value
        else:
            rows[-1] = rows[-1] + value

    def _build_tree(self):
        current_branch = self._form_data_rows[-1]["last_branch"]["parent"]
        for data_row in reversed(self._form_data_rows):

            if data_row is None:
                continue
            if id(self._form_data_rows[-1]) == id(data_row):
                continue

            # Запись

            data_row["branch"]["parent"] = current_branch
            for row in data_row["branch"]["rows"]:
                if type(row) == dict:
                    row["parent"] = current_branch
                current_branch["rows"].append(row)
            # Выбор новой текущей позиции

            new_current_branch = data_row["last_branch"]
            if (
                new_current_branch is None
                or data_row["last_branch"] == data_row["branch"]
            ):
                new_current_branch = current_branch

            if data_row["open_tag"]:
                new_current_branch = new_current_branch["parent"]
            current_branch = new_current_branch

        # Инвертируем результат

        for array in self._all_form_data_array:
            array.reverse()
            for i in range(len(array)):
                if type(array[i]) == str:
                    array[i] = array[i][::-1]

        if current_branch is None:
            # Исключение для чтения "красивого формата"
            self._form_data_tree = data_row["last_branch"]["parent"]
            del self._form_data_tree["rows"][-1]
        else:
            self._form_data_tree = current_branch["rows"][0]

    def _find_in_form_data_array(self, value):

        result = []
        for i in range(len(self._all_form_data_array)):
            array = self._all_form_data_array[i]
            for j in range(len(array)):
                if array[j] == value:
                    try:
                        index = result.index(i)
                    except ValueError:
                        index = None
                    if index is None:
                        result.append(i)
                    break

        return result

    def _find_form_data_array_by_id(self, value_id):

        for i in range(len(self._all_form_data_array)):
            array = self._all_form_data_array[i]
            if id(array) == value_id:
                return array

        return None

    def _remove_shit_from_control_panel(self, address):

        control_panel_data = self._all_form_data_array[address]
        if len(control_panel_data) == 2:
            return

        # Изменяется какая-то шляпа, диагностировано на EDI

        if control_panel_data[0] == "e69bf21d-97b2-4f37-86db-675aea9ec2cb":
            control_panel_name = control_panel_data[4]["rows"][1]
            control_panel_name = control_panel_name.replace('"', "")
            new_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, control_panel_name)
            control_panel_data[2]["rows"][1]["rows"][-4] = str(new_uuid)

        # Прочитаем командную панель во что-то

        control_panel = form_panel(control_panel_data)
        if control_panel is None:
            return
        if len(control_panel["item_parameters"]) == 0:
            return

        items_data_array = self._find_form_data_array_by_id(
            control_panel["items_data_Id"]
        )

        # Сгенерируем новые ID

        itemsID = {}
        for item in control_panel["items"]:
            index = control_panel["items"].index(item)
            itemKey = item["name"] + "_" + str(index)
            UUID = uuid.uuid5(uuid.NAMESPACE_DNS, itemKey)
            item["newID"] = str(UUID)
            item["index"] = index
            itemsID[item["id"]] = item

        # Подготовка к сортировке

        for parm in control_panel["item_parameters"]:
            item = itemsID[parm["id"]]
            parm["newID"] = item["newID"]
            parm["branch"] = items_data_array[parm["index"]]
            parm["itemindex"] = item["index"]
            parm["item_group_data_id"] = item["group_data_id"]
            parm["item_group_data_id_index"] = item["group_data_idIndex"]

        item_params_sorted = [] + control_panel["item_parameters"]
        item_params_sorted.sort(key=lambda i: i["itemindex"])

        # Перестановка и изменение UUID

        i = -1
        begin = control_panel["item_parameters"][0]["index"]
        end = control_panel["item_parameters"][-1]["index"]
        for j in range(begin, end + 1):

            i = i + 1
            param_data_Id = item_params_sorted[i]["data_id"]
            param_new_uuid = item_params_sorted[i]["newID"]
            param_branch = item_params_sorted[i]["branch"]
            item_group_data_id = item_params_sorted[i]["item_group_data_id"]
            item_group_data_id_index = item_params_sorted[i]["item_group_data_id_index"]

            # изменение UUID

            param_data_array = self._find_form_data_array_by_id(param_data_Id)
            param_data_array[1] = param_new_uuid
            item_group_data_array = self._find_form_data_array_by_id(item_group_data_id)
            item_group_data_array[item_group_data_id_index] = param_new_uuid

            # Перестановка

            items_data_array[j] = param_branch

    def _write_branch(self, branch, file):

        if self._form_data_tree == branch:
            file.write("{")
        else:
            file.write("\r\n{")

        count_of_row = len(branch["rows"])
        is_base64 = False

        if count_of_row > 0:
            first_row = branch["rows"][0]
            if type(first_row) == str and first_row[0:8] == "#base64:":
                is_base64 = True

        for i in range(count_of_row):

            if i != 0 and i != count_of_row and not is_base64:
                file.write(",")

            row = branch["rows"][i]
            if type(row) == dict:
                self._write_branch(row, file)
            elif is_base64:
                self._form_data_level = 0
                file.write(row)
                if i != count_of_row - 1:
                    file.write("\r\r\n")
            else:
                self._form_data_level = 0
                file.write(row)

        if self._form_data_level == 1:
            self._form_data_level = 0
            file.write("\r\n")

        file.write("}")
        self._form_data_level = 1

    def _write_branch_pretty(self, branch, file):

        self._form_data_level = self._form_data_level + 1

        otst = ""

        for i in range(self._form_data_level):
            if i != 0:
                otst = otst + "\t"

        if self._form_data_tree == branch:
            file.write(otst + "{")
        else:
            file.write("\r\n" + otst + "{")

        count_of_row = len(branch["rows"])
        is_base64 = False

        if count_of_row > 0:
            first_row = branch["rows"][0]
            if type(first_row) == str and first_row[0:8] == "#base64:":
                is_base64 = True

        for i in range(count_of_row):

            row = branch["rows"][i]
            if type(row) == dict:
                self._write_branch_pretty(row, file)
                if i != count_of_row - 1:
                    file.write(",")
            elif is_base64:
                if i == 0:
                    file.write("\r\n" + otst + "\t")
                file.write(row)
            else:
                file.write("\r\n" + otst + "\t")
                file.write(row)
                if i != count_of_row - 1:
                    file.write(",")

        file.write("\r\n" + otst + "}")

        self._form_data_level = self._form_data_level - 1

    def read(self):

        # Чтение строк данных формы в ветки

        bytes_ = min(32, os.path.getsize(self._form_data_path))
        raw = open(self._form_data_path, "rb").read(bytes_)
        if raw.startswith(codecs.BOM_UTF8):
            file = codecs.open(self._form_data_path, "r", encoding="utf-8-sig")
        else:
            file = codecs.open(self._form_data_path, "r", encoding="utf-8")

        self._form_data_lines = file.readlines()
        self._form_data_rows = [None] * len(self._form_data_lines)

        with ThreadPool() as pool:
            pool.map(self._read_rows, range(len(self._form_data_lines)))

        # Объединение веток

        self._build_tree()

    def marshal(self):

        # Что-то итерируется при каждом пересохранении

        Shit1 = self._form_data_tree["rows"][1]["rows"]
        Shit1[10] = "1"

        # e69bf21d-97b2-4f37-86db-675aea9ec2c - командная панель

        control_panel_in_data_array = self._find_in_form_data_array(
            "e69bf21d-97b2-4f37-86db-675aea9ec2cb"
        )
        for address in control_panel_in_data_array:
            self._remove_shit_from_control_panel(address)

        # 6ff79819-710e-4145-97cd-1618da79e3e2 - кнопка в режим меню

        control_panel_in_data_array = self._find_in_form_data_array(
            "6ff79819-710e-4145-97cd-1618da79e3e2"
        )
        for address in control_panel_in_data_array:
            self._remove_shit_from_control_panel(address)

    def write(self, file_name):
        file = codecs.open(file_name, "w+", "utf-8-sig")
        self._form_data_level = 0
        self._write_branch(self._form_data_tree, file)

    def write_pretty(self, file_name):
        file = codecs.open(file_name, "w+", "utf-8-sig")
        self._form_data_level = -1
        self._write_branch_pretty(self._form_data_tree, file)


def form_panel(data):

    control_panel = {}

    # Параметры элементов формы
    item_parameters = []
    items = []

    # Инициализация объекта
    # Неупорядоченная коллекция

    if data[0] == "e69bf21d-97b2-4f37-86db-675aea9ec2cb":
        items_data = data[2]["rows"][1]["rows"][7]["rows"]
    elif data[0] == "6ff79819-710e-4145-97cd-1618da79e3e2":
        menu_mode = data[2]["rows"][1]["rows"][11]
        if menu_mode == "0":
            return
        items_data = data[2]["rows"][1]["rows"][12]["rows"]
    else:
        raise IOError("что ты мне суешь?")

    items_param_count = int(items_data[4])
    for i in range(5, 5 + items_param_count):
        items_param_data = items_data[i]["rows"]
        items_param = {}
        items_param["id"] = items_param_data[1]
        items_param["data_id"] = id(items_param_data)
        items_param["index"] = i

        item_parameters.append(items_param)

    # Упорядоченная коллекция
    items_group = []
    items_groupCount = int(items_data[5 + items_param_count])
    for i in range(6 + items_param_count, 6 + items_param_count + items_groupCount):
        items_group.append(items_data[i])

    # Заполнение массив элементов
    for item_group in items_group:

        item_group_data = item_group["rows"]
        items_count = int(item_group_data[4])
        for i in range(5, 5 + items_count * 2, 2):
            item = {}
            item["id"] = item_group_data[i]
            item["name"] = item_group_data[i + 1]["rows"][1]
            item["name"] = item["name"].replace('"', "")
            item["data_id"] = id(item_group_data[i + 1]["rows"])

            item["group_data_id"] = id(item_group_data)
            item["group_data_idIndex"] = i

            items.append(item)

    control_panel["items_data_Id"] = id(items_data)
    control_panel["items"] = items
    control_panel["item_parameters"] = item_parameters

    return control_panel


# def afterUnpackForms(formPath):
#
#    newForm = Form(form_data_path)
#    newForm.read()
#    newForm.remove_shit()
#    newForm.writePretty(formPrettydata_path)
#
#
#
# def packForms(formPath, v8unpackpath):
#
#    formDirName = os.path.dirname(formPath)
#
#    form_data_path = os.path.normpath(formDirName + '/form.data')
#    formPrettydata_path = os.path.normpath(formDirName + '/form.prettydata')
#
#    # Генерация файлов для unpack из исходников
#
#    prettyForm = Form(formPrettydata_path)
#    prettyForm.read()
#    prettyForm.write(form_data_path)
#
#    # Генерация заголовков
#
#    fileHeaderPath = os.path.normpath(formDirName + '/FileHeader')
#    FileHeaderHex = binascii.unhexlify('FFFFFF7F000200000200000000000000')
#
#    FileHeader = open(fileHeaderPath, 'wb')
#    FileHeader.write(FileHeaderHex)
#    FileHeader.close()
#
#    formHeaderPath = os.path.normpath(formDirName + '/form.header')
#    FormHeaderHex = binascii.unhexlify(
#        '80F3B4A62C43020080F3B4A62C4302000000000066006F0072006D0000000000'
#    )
#
#    FormHeader = open(formHeaderPath, 'wb')
#    FormHeader.write(FormHeaderHex)
#    FormHeader.close()
#
#    moduleHeaderPath = os.path.normpath(formDirName + '/module.header')
#    moduleHeaderHex = binascii.unhexlify(
#        '80F3B4A62C43020080F3B4A62C430200000000006D006F00640075006C00650000000000'
#    )
#
#    moduleHeader = open(moduleHeaderPath, 'wb')
#    moduleHeader.write(moduleHeaderHex)
#    moduleHeader.close()
#
#    # Сборка бинарной формы из исходников, перед сборкой обработки
#
#    moduleBslPath = os.path.join(formDirName, 'module.bsl')
#    moduledata_path = os.path.join(formDirName, 'module.data')
#    formBinPath = os.path.join(formDirName, 'Form.bin')
#
#    if os.path.exists(moduledata_path):
#        os.remove(moduledata_path)
#
#    os.rename(moduleBslPath, moduledata_path)
#
#    if os.path.exists(moduleBslPath):
#        os.remove(moduleBslPath)
#
#    v8unpackpath = os.path.normpath(v8unpackpath)
#
#    сmdStr = f'""{v8unpackpath}" -PA "{formDirName}" "{formBinPath}""'
#
#    if ItsLinux:
#        сmdStr = сmdStr.replace('"', '')
#        сmdStr = сmdStr.replace("'", '')
#
#    result = os.system(сmdStr)
#    if result != 0:
#        raise Exception('Не удалось собрать ' + formDirName)
#

import tempfile
import pathlib
import os
from multiprocessing.dummy import Pool as ThreadPool

from .tools.v8file import build_form as build_form, dump_file as dump_v8file
from .tools.v8form import Form


def unpack_form(file):
    """
    Помогает распаковать файл Form.bin
    """
    assert os.path.exists(file)

    file_dir = os.path.dirname(file)
    from_pretty = os.path.join(file_dir, "form.prettydata")
    module_bsl = os.path.join(file_dir, "module.bsl")

    with tempfile.TemporaryDirectory() as tmpdir:

        dump_v8file(v8file=file, src_dir=tmpdir)

        form_data = os.path.join(tmpdir, "form.data")
        module_data = os.path.join(tmpdir, "module.data")

        assert os.path.exists(form_data)
        assert os.path.exists(module_data)

        # Запись красивой формы

        form = Form(form_data_path=form_data)
        form.read()
        form.marshal()
        form.write_pretty(from_pretty)

        # Копирование модуля

        if os.path.exists(module_bsl):
            os.remove(module_bsl)

        os.rename(module_data, module_bsl)

        return from_pretty, module_bsl


def pack_form(file_bsl, file_pretty):
    """
    Помогает собрать файл Form.bin из form.prettydata
    """

    assert os.path.exists(file_bsl)
    assert os.path.exists(file_pretty)

    file_dir = os.path.dirname(file_bsl)
    form_bin = os.path.join(file_dir, "Form.bin")

    with tempfile.TemporaryDirectory() as tmpdir:

        form_data = os.path.join(tmpdir, "form.data")

        form = Form(form_data_path=file_pretty)
        form.read()
        form.write(form_data)

        build_form(v8file=form_bin, module_data=file_bsl, form_data=form_data)

    assert os.path.exists(form_bin)

    return form_bin
    ...


def unpack_forms(folder):
    """
    Разбирает все Form.bin в каталоге
    """
    binaries_forms = _find_files(folder, "Form.bin")
    with ThreadPool() as pool:
        data = pool.map(unpack_form, binaries_forms)
    result = []
    for i in range(len(binaries_forms)):
        # *.bin, *.prettydata, *.bsl
        result.append((binaries_forms[i], data[i][0], data[i][1],))
    return result


def pack_forms(folder):
    """
    Собирает все Form.bin из form.prettydata, module.bsl
    """
    forms = _find_files(folder, "form.prettydata")
    with ThreadPool() as pool:
        data = pool.map(_pack_form, forms)
    result = []
    for i in range(len(forms)):
        # *.bin, *.prettydata, *.bsl
        result.append((data[i][0], forms[i], data[i][1],))
    return result


def _find_files(path, mask, mask_ignore=".git/", recursive=True):
    result = []
    if recursive:
        mask = "**/" + mask
    for i in pathlib.Path(path).glob(mask):
        if mask_ignore not in str(i):
            result.append(str(i))

    return result


def _pack_form(file_pretty):
    file_dir = os.path.dirname(file_pretty)
    file_bsl_lower = os.path.join(file_dir, "module.bsl")
    file_bsl_upper = os.path.join(file_dir, "Module.bsl")
    if os.path.exists(file_bsl_upper):
        file_bsl = file_bsl_upper
    else:
        file_bsl = file_bsl_lower
    return pack_form(file_bsl=file_bsl, file_pretty=file_pretty), file_bsl

# unp1c

Сбор/разбор бинарей 1С:Предприятие

## Установка

```bash
# из репозитория
pip install .
# из pypi.kontur.host
pip install --index-url https://pypi.kontur.host kontur-unp1c
```

## Использование

Работа с бинарными файлами

```py
from kontur.unp1c import build_file, dump_file

form_bin = "src/Form.bin"
form_src = "src"
                                              # переход с v8unpack 
dump_file(v8file=form_bin, src_dir=form_src)  # os.system(f"v8unpack -U {form_bin} {form_src}")
build_file(v8file=form_bin, src_dir=form_src) # os.system(f"v8unpack -PA {form_src} {form_bin}")
```

Работа с каталогами исходников

```py
from kontur.unp1c import pack_forms, unpack_forms

unpack_forms("src")
pack_forms("src")
```

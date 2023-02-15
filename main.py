#!/usr/bin/env python3
# coding: utf-8

import json
import urllib.request
from pathlib import Path

PATH_TO_EXAMPLE_CRATE = Path(__file__).parent.joinpath("./example.json").resolve()


def main() -> None:
    with PATH_TO_EXAMPLE_CRATE.open("r") as f:
        crate = json.load(f)
    entity = crate["@graph"][0]
    entity_ctx_location = entity["@context"]
    with urllib.request.urlopen(entity_ctx_location) as f:
        ctx = json.load(f)
    entity_type_location = ctx["@context"].get(entity["@type"])
    if entity_type_location is None:
        raise ValueError(f"Could not find type {entity['@type']}")

    # type_loc to module_loc
    module_loc = entity_type_location.split("#")[0].replace(".yml", ".py")
    with urllib.request.urlopen(module_loc) as f:
        module = f.read().decode("utf-8")

    # このパターンは失敗する
    # module_globals = {}  # type: ignore
    # module_locals = {}  # type: ignore
    # exec(module, module_globals, module_locals)
    # print(module_globals)
    # print(module_locals)

    module_dir = Path(__file__).parent.joinpath("remote_module")
    module_dir.mkdir(exist_ok=True)
    module_path = module_dir.joinpath("module.py")
    with module_path.open("w") as f:
        f.write(module)
    module_globals = {}  # type: ignore
    module_locals = {}  # type: ignore
    exec("from remote_module.module import Module", module_globals, module_locals)
    module_ins = module_locals["Module"](msg=entity["msg"])
    module_ins.print_msg()


if __name__ == "__main__":
    main()

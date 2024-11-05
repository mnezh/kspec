import argparse
import importlib
import inspect
import pathlib
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        "-o",
        type=argparse.FileType("x"),
        default=sys.stdout,
        metavar="PATH",
        help="Output file (default: standard output)",
    )
    parser.add_argument("classname")
    return parser.parse_args()


def get_class_name(args: argparse.Namespace) -> str:
    class_name: str = args.classname
    return class_name[2:] if class_name.startswith("V1") else class_name


def class_has_metadata(module_name: str, import_class_name: str):
    module = importlib.import_module(module_name)
    imported_class = getattr(module, import_class_name)
    assert inspect.isclass(
        imported_class
    ), f"{module_name}.{import_class_name} should be a class"
    return hasattr(imported_class, "metadata")


def get_template(template_name) -> str:
    with open(pathlib.Path(__file__).parent / template_name) as f:
        return f.read()


def generate(template_name, module_name, import_class_name, base_class, class_name):
    template = get_template(template_name)
    return template.format(
        module_name=module_name,
        import_class_name=import_class_name,
        base_class=base_class,
        class_name=class_name,
    )


def main():
    args = parse_args()
    class_name = get_class_name(args)
    import_class_name = f"V1{class_name}"
    module_name = (
        "kubernetes.client.models.v1_"
        + re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).lower()
    )
    if class_has_metadata(module_name, import_class_name):
        base_class = "KubernetesMetadataObjectWrapper"
    else:
        base_class = "KubernetesObjectWrapper"
    args.output.write(
        generate(
            "class.template", module_name, import_class_name, base_class, class_name
        )
    )


if __name__ == "__main__":
    main()

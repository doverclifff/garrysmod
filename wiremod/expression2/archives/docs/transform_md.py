# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

from os import curdir
from glob import glob
from pathlib import Path

_MarkdownFileDescriptorTablePrototype = {
    "header": {"name": "", "extension": [], "bytes": 0, "path": ""},
    "data": {"body": [], "lines": 0},
}


def main() -> None:
    output_filename = "expression2_language_reference.txt"
    globbed = glob("docs/*.md", root_dir=curdir)
    print(f"File name: {output_filename}")
    print("File extension: .txt")
    print("MIME type: text/plain")
    print("Creation date: 01 January 2026")
    print("\n----")
    print(
        "\nExpression 2 Language Reference - adapted from the Expression 2 GitHub wiki"
    )
    print(
        "\nThis plain-text document is an adaptation of several\n\
Markdown-formatted documents from the official Expression 2 Language Reference\n\
into a single monolithic plain-text document."
    )
    print(
        "\nIt is intended to be used by artificial intelligence technologies, such as\n\
large language models (LLMs). Some modifications have been made from the\n\
original documents in order to adapt them for AI use."
    )
    print(f"\nThis file was compiled from {len(globbed)} text sources:")
    for idx, rel_pth in enumerate(globbed):
        print(f"    {idx}. {rel_pth[:-3]}")
    print("\n", end="")

    mapTypeStringTransforms = [
        [
            "Number",
            "String",
            "ComplexNumber",
            "Angle",
            "Vector",
            "Vector2",
            "Vector4",
            "Matrix",
            "Matrix2",
            "Matrix4",
            "Quaternion",
            "Array",
            "Table",
            "Entity",
            "Bone",
            "WireLink",
            "RangerData",
        ],
        [
            "NumberType",
            "StringType",
            "ComplexType",
            "AngleType",
            "VectorType",
            "Vector2Type",
            "Vector4Type",
            "MatrixType",
            "Matrix2Type",
            "Matrix4Type",
            "QuaternionType",
            "ArrayType",
            "TableType",
            "EntityType",
            "BoneType",
            "WirelinkType",
            "RangerDataType",
        ],
    ]
    for idx, rel_pth in enumerate(globbed):
        rel_pth = Path(rel_pth)
        abs_pth = Path(rel_pth).resolve()
        this_file_descriptor = _MarkdownFileDescriptorTablePrototype.copy()

        strings_from_file = []
        modified_strings = []
        with open(rel_pth, "r") as fd:
            strings_from_file = fd.read(-1).splitlines()
        assert strings_from_file != []

        for line in strings_from_file:
            # Skip empty lines
            if line == "":
                continue
            if line == "<br>":
                continue
            if line == "[Jump to table of contents](#default-extensions)":
                continue
            if str(rel_pth) == "Prop-core.md":
                if line.startswith("[ref-"):
                    continue

            modified_line = line
            for k, v in zip(*mapTypeStringTransforms):
                # in all files:
                md_e2type_image_embedding = f'![{k}](Type-{k}.png "{k}")'
                plaintext_type_string = v
                # Replace embedded images which denote variable types with plaintext strings
                modified_line = modified_line.replace(
                    md_e2type_image_embedding, plaintext_type_string
                )
                # Special case to handle erroneously named Matrix2 embeddings
                modified_line = modified_line.replace(
                    '![Matrix4](Type-Matrix2.png "Matrix2")', "Matrix2Type"
                )
                modified_line = modified_line.lstrip("### ")
                modified_line = modified_line.strip(" ")

                # in Expression-2-*.md only:
                if (
                    str(rel_pth).startswith("Expression-2-")
                    and str(rel_pth)[-3:].lower() == ".md"
                ):
                    modified_line = modified_line.replace("```C++", "<start codeblock>")
                    modified_line = modified_line.replace(
                        "```ruby", "<start codeblock>"
                    )
                    modified_line = modified_line.replace(
                        "```golo", "<start codeblock>"
                    )
                    modified_line = modified_line.replace("```", "<end codeblock>")

                # in Prop-core.md only:
                if str(rel_pth) == "Prop-core.md":
                    # Replace embedded type images
                    prefix = "![image][ref-"
                    for kk, vv in zip(
                        [
                            "a",
                            "b",
                            "c",
                            "e",
                            "xm2",
                            "m",
                            "xm4",
                            "n",
                            "q",
                            "r",
                            "s",
                            "t",
                            "xv2",
                            "v",
                            "xv4",
                            "xrd",
                            "xwl",
                            "",
                        ],
                        [4, 14, 2, 13, 8, 7, 9, 0, 10, 11, 1, 12, 4, 5, 6, 16, 15],
                    ):
                        modified_line = modified_line.replace(
                            prefix + kk + "]", mapTypeStringTransforms[1][vv]
                        )
                    modified_line = modified_line.replace("||", " ")
                    modified_line = modified_line.strip("|")
                    modified_line = modified_line.replace(
                        "[props][ref-prp-typ]", "props"
                    )
                    modified_line = modified_line.replace(
                        "[Garry's mod][ref-gmod]", "Garry's Mod"
                    )
                    modified_line = modified_line.replace(
                        "[E2][ref-exp2]", "Expression 2"
                    )
                    modified_line = modified_line.replace(
                        "[find them here][ref-e2-data]!", "find them elsewhere."
                    )
                    modified_line = modified_line.replace(
                        "[console variables][ref-convar]", "convars"
                    )
                # Disallow backticks (they can cause issues with LLMs)
                modified_line = modified_line.replace("`", "")

            modified_strings.append(modified_line)
            processed_file_size = sum([len(s) for s in modified_strings])
            this_file_descriptor["header"]["name"] = str(rel_pth)[:-3]
            this_file_descriptor["header"]["extension"] = [".md", "Markdown"]
            this_file_descriptor["header"]["bytes"] = processed_file_size
            this_file_descriptor["header"]["path"] = abs_pth
            this_file_descriptor["data"]["body"] = modified_strings
            this_file_descriptor["header"]["lines"] = len(modified_strings)

        print("\n----\n")
        print(
            f"Source name: {this_file_descriptor['header']['name']}\nSource number: {idx}\nMIME: text/plain\nSize (bytes): {this_file_descriptor['header']['bytes']}\nLines: {this_file_descriptor['header']['lines']}"
        )
        for idx, s in enumerate(modified_strings):
            print(f"    {idx} {s}")


if __name__ == "__main__":
    main()

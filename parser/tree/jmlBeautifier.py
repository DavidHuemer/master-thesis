def beautify_jml(jml: str):
    if jml.startswith("```"):
        # jml is the whole jml without the first and last line
        # So we need to remove the first and last line
        jml = jml.split("\n")[1:-1]
        jml = "\n".join(jml)

    return jml

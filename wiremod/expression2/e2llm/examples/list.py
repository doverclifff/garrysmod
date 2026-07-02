import ollama as ol

response: ol.ListResponse = ol.list()

for idx, model in enumerate(response.models):
    mdl_name = model.model
    if len(model.model) > 60:
        mdl_name = f"{model.model[:60]}..."
    else:
        mdl_name = model.model
    s = f"{idx:>4}{':':<2}{mdl_name:<66} "

    if model.details:
        mdl_details = model.details
        mdl_family = mdl_details.family
        mdl_params = mdl_details.parameter_size
        mdl_quant = mdl_details.quantization_level
        s = s + f"{mdl_family:<16} {mdl_params:<8} {mdl_quant:<8} "
    s = s + f"{(model.size.real / 1024 / 1024):.2f} MiB"
    print(s)

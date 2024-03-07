from transformers import AutoTokenizer, BertModel, BertTokenizer, RobertaModel, RobertaTokenizerFast


def get_tokenlizer(text_encoder_type):
    if not isinstance(text_encoder_type, str):
        # print("text_encoder_type is not a str")
        if hasattr(text_encoder_type, "text_encoder_type"):
            text_encoder_type = text_encoder_type.text_encoder_type
        elif text_encoder_type.get("text_encoder_type", False):
            text_encoder_type = text_encoder_type.get("text_encoder_type")
        else:
            raise ValueError(
                "Unknown type of text_encoder_type: {}".format(type(text_encoder_type))
            )
    print("final text_encoder_type: {}".format(text_encoder_type))
    # tokenizer_path = "Grounded-Segment-Anything/huggingface/bert-base-uncased"
    # tokenizer = BertTokenizer.from_pretrained(tokenizer_path, use_fast=False)
    # return tokenizer
    tokenizer = AutoTokenizer.from_pretrained(text_encoder_type)
    return tokenizer


def get_pretrained_language_model(text_encoder_type):
    if text_encoder_type == "bert-base-uncased":
        # model_path = "Grounded-Segment-Anything/huggingface/bert-base-uncased/pytorch_model.bin"
        # return BertModel.from_pretrained(model_path)
        return BertModel.from_pretrained(text_encoder_type)
    if text_encoder_type == "roberta-base":
        return RobertaModel.from_pretrained(text_encoder_type)
    raise ValueError("Unknown text_encoder_type {}".format(text_encoder_type))

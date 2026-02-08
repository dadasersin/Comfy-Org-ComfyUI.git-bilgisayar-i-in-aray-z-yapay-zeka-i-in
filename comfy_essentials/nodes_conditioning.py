from comfy.comfy_types.node_typing import ComfyNodeABC, IO, InputTypeDict


class CLIPTextEncode(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(s) -> InputTypeDict:
        return {
            "required": {
                "text": (IO.STRING, {"multiline": True, "dynamicPrompts": True, "tooltip": "The text to be encoded."}),
                "clip": (IO.CLIP, {"tooltip": "The CLIP model used for encoding the text."})
            }
        }
    RETURN_TYPES = (IO.CONDITIONING,)
    OUTPUT_TOOLTIPS = ("A conditioning containing the embedded text used to guide the diffusion model.",)
    FUNCTION = "encode"

    CATEGORY = "conditioning"
    MAIN_CATEGORY = "Basic"
    DESCRIPTION = "Encodes a text prompt using a CLIP model into an embedding that can be used to guide the diffusion model towards generating specific images."
    SEARCH_ALIASES = ["text", "prompt", "text prompt", "positive prompt", "negative prompt", "encode text", "text encoder", "encode prompt"]

    def encode(self, clip, text):
        if clip is None:
            raise RuntimeError("ERROR: clip input is invalid: None\n\nIf the clip is from a checkpoint loader node your checkpoint does not contain a valid clip or text encoder model.")
        tokens = clip.tokenize(text)
        return (clip.encode_from_tokens_scheduled(tokens), )


NODE_CLASS_MAPPINGS = {
    "CLIPTextEncode": CLIPTextEncode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CLIPTextEncode": "CLIP Text Encode (Prompt)",
}

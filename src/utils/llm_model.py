import os
import json
from typing import Optional

import boto3
from botocore.exceptions import NoCredentialsError, ClientError, BotoCoreError
from dotenv import load_dotenv

load_dotenv()


class LLM_Model:

    def __init__(
        self,
        model_id=os.getenv("LLM_Model_Id"),
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    ):
        """Initialize the Bedrock Runtime client."""

        if not model_id:
            raise ValueError("LLM_Model_Id environment variable not set.")

        self.model_id = model_id

        self.bedrock_runtime = boto3.client(
            "bedrock-runtime",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def generate_response(
        self,
        user_query: str,
        system_prompt: str,
        context: str,
        max_tokens: int = 800,
        temperature: float = 0.7,
        top_p: Optional[float] = None,
    ) -> str:

        if not user_query.strip():
            return "Error: user_query must be a non-empty string."

        inference_cfg = {"maxTokens": max_tokens, "temperature": temperature}
        if top_p is not None:
            inference_cfg["topP"] = top_p

        try:
            
            response = self.bedrock_runtime.converse(
                modelId=self.model_id,
                system=[{"text": f"System Prompt:{system_prompt}"}],
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"text": f"Query:\n{user_query}"},
                            {"text": f"Context:\n{context}"},
                        ],
                    },
                ],
                inferenceConfig=inference_cfg,
            )
            content_blocks = (
                response.get("output", {}).get("message", {}).get("content", [])
            )
            print(response)

            texts = [
                block["text"]
                for block in content_blocks
                if isinstance(block, dict) and "text" in block
            ]

            return "\n".join(texts)

        except NoCredentialsError:
            return (
                "Error: No AWS credentials found. Configure via env vars, "
                "`aws configure`, or IAM role."
            )
        except (ClientError, BotoCoreError) as sdk_err:
            return f"Error: AWS SDK error: {sdk_err}"
        except Exception as e:
            return f"Error: Unexpected error: {str(e)}"
    def health_check(self) -> bool:
        try:
            _ = self.generate_response("just a health check","just say hi","")
            return True
        except Exception:
            return False
    # def classify_query(
    #     self,
    #     user_query: str,
    #     max_tokens: int = 5,
    #     temperature: float = 1
    # ) -> str:

    #     system = (
    #         "You are a strict prompt classifier "
    #         "Classify the user query into one of EXACTLY these labels: "
    #         "TRAVEL, NOT_TRAVEL, INAPPROPRIATE. "
    #         "If user speak about travel means only TRAVEL reponse otherwise NOT_TRAVEL AND INAPPROPRIATE, fully analze the sentence and decide for one word prompt just give NOT_TRAVEL"
    #         "Output ONLY the label with no punctuation or explanation."
    #     )

    #     messages = [
    #         {
    #             "role": "user",
    #             "content": [
    #                 {"text": f"Query:\n{user_query}\n\nReply with only one label: TRAVEL or NOT_TRAVEL or INAPPROPRIATE"}
    #             ],
    #         }
    #     ]

    #     inference_cfg = {"maxTokens": max_tokens, "temperature": temperature}

    #     resp = self.bedrock_runtime.converse(
    #         modelId=self.model_id,
    #         system=[{"text": system}],
    #         messages=messages,
    #         inferenceConfig=inference_cfg,
    #     )
    #     content_blocks = resp.get("output", {}).get("message", {}).get("content", [])
    #     label = ""
    #     for b in content_blocks:
    #         if isinstance(b, dict) and "text" in b:
    #             label += b["text"].strip().upper()

    #     label = label.strip()
    #     print("label  ",label)
    #     return label
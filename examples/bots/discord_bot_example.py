# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========

from camel.agents import ChatAgent
from camel.bots.discord_bot import DiscordBot
from camel.messages import BaseMessage
from camel.retrievers import AutoRetriever
from camel.types import StorageType


def main(model=None) -> None:
    assistant_sys_msg = BaseMessage.make_assistant_message(
        role_name="Assistant",
        content="You are a helpful assistant.",
    )

    agent = ChatAgent(assistant_sys_msg, model_type=model)
    auto_retriever = AutoRetriever(
        url_and_api_key=("Your Milvus URI","Your Milvus Token"),
        storage_type=StorageType.MILVUS)
    bot = DiscordBot(agent,auto_retriever=auto_retriever,content_input_paths=["local_data/"])
    bot.run()


if __name__ == "__main__":
    main()

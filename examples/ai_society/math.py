import json
from colorama import Fore

from camel.societies import RolePlaying
from camel.utils import print_text_animated


def main(model=None, chat_turn_limit=50) -> None:
    # Load JSON data
    data = data = [
        {
            "year": "2010",
            "category": "（新课标）",
            "question": "1. （5 分) 已知集合 $A=\\{{x \\in R | |x| \\leqslant 2\\}}$, B=\\{{x \\in Z | \\sqrt{{x}} \\leqslant 4\\}}$, 则 $A \\cap B=(\\quad$ ）\nA. $(0,2)$\nB. $[0,2]$\nC. $\\{{0,2\\}}$\nD. $\\{{0,1,2\\}}$\n",
            "score": 5,
            "index": 0
        }
    ]
    
    # Define the task prompt from JSON data
    task_prompt = data[0]['question']

    # Initialize the role-playing session with teacher and student roles
    role_play_session = RolePlaying(
        assistant_role_name="Student",
        assistant_agent_kwargs=dict(model=model),
        user_role_name="Teacher",
        user_agent_kwargs=dict(model=model),
        task_prompt=task_prompt,
        with_task_specify=True,
        task_specify_agent_kwargs=dict(model=model),
    )

    # Start the interaction
    print(Fore.GREEN + f"Teacher sys message:\n{role_play_session.user_sys_msg}\n")
    print(Fore.BLUE + f"Student sys message:\n{role_play_session.assistant_sys_msg}\n")
    print(Fore.YELLOW + f"Original task prompt:\n{task_prompt}\n")
    print(Fore.RED + f"Final task prompt:\n{role_play_session.task_prompt}\n")

    n = 0
    input_msg = role_play_session.init_chat()
    while n < chat_turn_limit:
        n += 1
        assistant_response, user_response = role_play_session.step(input_msg)

        if assistant_response.terminated:
            print(Fore.GREEN + "Student terminated. Reason: " + assistant_response.info['termination_reasons'])
            break
        if user_response.terminated:
            print(Fore.BLUE + "Teacher terminated. Reason: " + user_response.info['termination_reasons'])
            break

        print_text_animated(Fore.BLUE + f"Teacher:\n\n{user_response.msg.content}\n")
        print_text_animated(Fore.GREEN + "Student:\n\n" + assistant_response.msg.content + "\n")

        if "CAMEL_TASK_DONE" in user_response.msg.content:
            break

        input_msg = assistant_response.msg

    # Save the session result to JSON
    session_result = {
        "question": task_prompt,
        "answer": assistant_response.msg.content.strip()  # Assuming this contains the answer
    }
    with open("session_result.json", "w") as f:
        json.dump(session_result, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()

import asyncio

from app.ai.tools import (
    date_tool,
    location_tool,
    weather_tool,
)

tool_map = {
    "date_tool": date_tool,
    "location_tool": location_tool,
    "weather_tool": weather_tool,
}

TOOL_DEPENDENCIES = {
    "weather_tool": ["location_tool"],
    "date_tool": [],
    "location_tool": [],
}


async def call_tool(tool_name: str, args: dict):
    tool = tool_map.get(tool_name)

    if tool is None:
        return {
            "success": False,
            "message": f"Tool {tool_name} 不存在"
        }

    try:

        result = await tool.ainvoke(args)

        return result

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


async def execute(plan: dict):
    tools = plan.get("tools", [])

    executed = {}

    while len(executed) < len(tools):

        runnable = []

        for tool in tools:

            name = tool["name"]

            if name in executed:
                continue

            deps = TOOL_DEPENDENCIES.get(name, [])

            if all(dep in executed for dep in deps):
                runnable.append(tool)

        if not runnable:
            break

        tasks = []

        task_names = []

        for tool in runnable:

            name = tool["name"]

            args = tool.get("args", {}).copy()

            # ==========================
            # weather 依赖 location
            # ==========================

            if name == "weather_tool":

                location = executed.get("location_tool")

                if location is None:
                    executed[name] = {
                        "success": False,
                        "message": "location_tool 未执行"
                    }

                    continue

                if not location.get("success"):
                    executed[name] = {
                        "success": False,
                        "message": location.get(
                            "message",
                            "地点解析失败"
                        )
                    }

                    continue

                args["location"] = (
                        location.get("district")
                        or location.get("city")
                        or location.get("province")
                )

            task_names.append(name)

            tasks.append(

                asyncio.create_task(

                    call_tool(
                        name,
                        args,
                    )

                )

            )

        if tasks:

            results = await asyncio.gather(*tasks)

            for name, result in zip(task_names, results):
                executed[name] = result

    print("\n==============================")
    print("Tool Results")
    print(executed)
    print("==============================\n")

    return executed

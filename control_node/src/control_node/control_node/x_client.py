import asyncio

from rclpy.action import ActionClient


class ActionClientX(ActionClient):
    feedback_queue = asyncio.Queue()

    async def feedback_cb(self, msg):
        await self.feedback_queue.put(msg)

    async def send_goal_async(self, goal_msg):
        goal_future = super().send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_cb
        )
        client_goal_handle = await asyncio.ensure_future(goal_future)
        if not client_goal_handle.accepted:
            raise Exception("Goal rejected.")
        result_future = client_goal_handle.get_result_async()
        while True:
            feedback_future = asyncio.ensure_future(self.feedback_queue.get())
            tasks = [result_future, feedback_future]
            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            if result_future.done():
                result = result_future.result().result
                yield (None, result)
                break
            else:
                feedback = feedback_future.result().feedback
                yield (feedback, None)
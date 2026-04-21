import pytest
from cmp3103_tidy_bot.tidy_bot_node import TidyBotNode
import rclpy

def test_node_init():
    rclpy.init()
    node = TidyBotNode()
    assert node.state == "SEARCHING"
    node.destroy_node()
    rclpy.shutdown()

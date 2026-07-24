import pytest
from tools.file_ops import ReadFileTool

@pytest.mark.asyncio
async def test_read_file_tool_missing():
    tool = ReadFileTool()
    result = await tool.execute("does_not_exist.txt")
    assert result.success == False
    assert "not found" in result.error

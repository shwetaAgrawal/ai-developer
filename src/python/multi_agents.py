import asyncio
from typing import List, Any
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.agents.strategies.termination.termination_strategy import TerminationStrategy


kernel = Kernel()


#Create a Business Analyst Agent [ChatCompletionAgent] and add it to the Agents List.
#ChatCompletionAgent takes Instructions, a Name (No Spaces allowed), and the Kernel.

# Create a Software Engineer Agent [ChatCompletionAgent] and add it to the Agents List.
# ChatCompletionAgent takes Instructions, a Name (No Spaces allowed), and the Kernel.

# Create a Product Owner Agent [ChatCompletionAgent] and add it to the Agents List.
# ChatCompletionAgent takes Instructions, a Name (No Spaces allowed), and the Kernel.

# Create Agent Group Chat [AgentGroupChat]

user_input = "Create a simple calculator app"

class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""

    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate."""
        raise NotImplementedError("Must implement this method.")
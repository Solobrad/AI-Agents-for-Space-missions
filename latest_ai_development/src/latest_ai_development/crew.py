import os                      # ADDED: For file path handling
import json
from typing import Any, Dict
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import Extra
from crewai_tools import SerperDevTool


# Define a custom agent class that allows extra fields


class CustomAgent(Agent):
    class Config:
        extra = Extra.allow


class DatabaseAgent(CustomAgent):
    db_connection: Any = None
    data: Dict[str, Any] = {}

    class Config:
        extra = Extra.allow


@CrewBase
class LatestAiDevelopment():
    """LatestAiDevelopment crew for Space Resource Management"""

    # Configuration files for agents and tasks
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def database_agent(self) -> Agent:
        agent_instance = DatabaseAgent(
            config=self.agents_config['database_agent'],
            verbose=True,
        )
        agent_instance.json_file = os.path.join(os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..')), "space_missions.json")
        print(f"JSON file path: {agent_instance.json_file}")
        return agent_instance

    @agent
    def researcher(self) -> Agent:
        researcher_agent = CustomAgent(
            config=self.agents_config['researcher'],
            verbose=True,
            tools=[SerperDevTool()]
        )
        return researcher_agent

    @agent
    def mission_integration_strategist(self) -> Agent:
        mis_agent = CustomAgent(
            config=self.agents_config['mission_integration_strategist'],
            verbose=True
        )
        return mis_agent

    @agent
    def resource_management_specialist(self) -> Agent:
        rm_agent = CustomAgent(
            config=self.agents_config['resource_management_specialist'],
            verbose=True
        )
        return rm_agent

    @agent
    def reporting_analyst(self) -> Agent:
        report_agent = CustomAgent(
            config=self.agents_config['reporting_analyst'],
            verbose=True
        )
        return report_agent

    # Task for database handling: extract and share database data and anomalies.
    @task
    def database_task(self) -> Task:
        def run_database_task(context: Dict[str, Any]) -> str:
            # Access the pre-initialized agent instance from the crew
            db_agent = self.database_agent()
            json_file = db_agent.json_file

            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
            except Exception as e:
                return f"Error loading JSON: {str(e)}"

            # Update the agent's data and shared context
            db_agent.data = data
            context["database_data"] = data
            return f"Successfully loaded {len(data)} records."

        return Task(config=self.tasks_config['database_task'], run=run_database_task)

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])

    @task
    def mission_integration_task(self) -> Task:
        task_config = self.tasks_config['mission_integration_task']
        return Task(config=task_config)

    @task
    def resource_management_task(self) -> Task:
        return Task(config=self.tasks_config['resource_management_task'])

    # Task for reporting: collate all shared outputs into a final report.
    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            # This is the file that will be contain the final report.
            output_file='output/report.md'
        )

    @crew
    def crew(self) -> Crew:
        # Instantiate agents
        db_agent = self.database_agent()
        researcher_agent = self.researcher()
        mis_agent = self.mission_integration_strategist()
        rm_agent = self.resource_management_specialist()
        report_agent = self.reporting_analyst()

        # Initialize an empty shared context dictionary.
        shared_context: Dict[str, Any] = {}

        # Return the Crew with sequential tasks that update the shared context.
        return Crew(
            agents=[db_agent, researcher_agent,
                    mis_agent, rm_agent, report_agent],
            tasks=[
                self.database_task(),
                self.research_task(),
                self.mission_integration_task(),
                self.resource_management_task(),
                self.reporting_task()
            ],
            shared_context=shared_context,
            process=Process.sequential,
            verbose=True,
        )

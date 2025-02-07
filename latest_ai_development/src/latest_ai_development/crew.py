from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class LatestAiDevelopment():
    """LatestAiDevelopment crew for Space Resource Management"""

    # Configuration files for agents and tasks (ensure these YAML files include keys:
    # 'researcher', 'reporting_analyst', and 'optimization_specialist' for agents,
    # and 'research_task', 'reporting_task', and 'optimization_task' for tasks)
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Agent for the researcher role
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True
        )

    # Agent for the reporting analyst role
    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True
        )

    # Agent for the optimization specialist role
    @agent
    # Added: optimization_specialist agent
    def optimization_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['optimization_specialist'],
            verbose=True
        )

    # Agent for the Mission Integration Strategist role
    @agent
    def mission_integration_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['mission_integration_strategist'],
            verbose=True
        )

    # Agent for the Anomaly & Contingency Manager role
    @agent
    def anomaly_contingency_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['anomaly_contingency_manager'],
            verbose=True
        )

    # Task for conducting research
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    # Task for generating the report
    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            output_file='report.md'
        )

    # New task for optimization analysis
    @task
    def optimization_task(self) -> Task:  # Added: optimization task
        return Task(
            config=self.tasks_config['optimization_task'],
        )

    # Task for mission integration strategy
    @task
    def mission_integration_task(self) -> Task:
        return Task(
            config=self.tasks_config['mission_integration_task'],
        )

    # Task for anomaly and contingency planning
    @task
    def anomaly_contingency_task(self) -> Task:
        return Task(
            config=self.tasks_config['anomaly_contingency_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew with all agents and tasks"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorators
            tasks=self.tasks,    # Automatically created by the @task decorators
            process=Process.sequential,
            verbose=True,
            # Alternatively, you can use a hierarchical process:
            # process=Process.hierarchical,
        )

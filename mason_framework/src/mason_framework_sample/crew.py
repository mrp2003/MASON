from crewai import Agent, Crew, Process, Task # type: ignore
from crewai_tools import FileWriterTool # type: ignore
from crewai.project import CrewBase, agent, crew, task # type: ignore

@CrewBase
class MasHumanevalOpenai():
	
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def input_parser(self) -> Agent:
		return Agent(
			config=self.agents_config['input_parser'],
			tools=[],
        )

	@agent
	def requirements_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['requirements_analyzer'],
			tools=[],
		)

	@agent
	def code_generator(self) -> Agent:
		return Agent(
			config=self.agents_config['code_generator'],
			tools=[],
		)

	@agent
	def code_validator(self) -> Agent:
		return Agent(
			config=self.agents_config['code_validator'],
			tools=[],
		)

	@agent
	def file_output_specialist(self) -> Agent:
		file_writer_tool = FileWriterTool()
		return Agent(
			config=self.agents_config['file_output_specialist'],
			tools=[file_writer_tool]
		)

	@task
	def parse_input_task(self) -> Task:
		return Task(
			config=self.tasks_config['parse_input_task'],
			tools=[],
		)

	@task
	def requirements_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['requirements_analysis_task'],
			tools=[],
		)

	@task
	def code_generation_task(self) -> Task:
		return Task(
			config=self.tasks_config['code_generation_task'],
			tools=[],
		)

	@task
	def code_validation_task(self) -> Task:
		return Task(
			config=self.tasks_config['code_validation_task'],
			tools=[],
		)

	@task
	def file_output_task(self) -> Task:
		return Task(
			config=self.tasks_config['file_output_task'],
			tools=[],
		)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			process=Process.sequential,
			verbose=True,
		)
from datetime import UTC
from datetime import datetime
from datetime import timedelta

from faker import Faker
from faker.providers import BaseProvider

from fakeapi.tasks.enums import TaskStatus


class TaskProvider(BaseProvider):
    titles: list[str] = [
        "AI-Powered CRM System",
        "E-commerce Platform Revamp",
        "Cloud Migration Strategy",
        "Cybersecurity Enhancement",
        "Blockchain Payment Integration",
        "Automated Customer Support",
        "SEO Optimization Initiative",
        "Green Energy Transition",
        "IoT Smart Home Project",
        "Data Analytics Dashboard",
        "HR Onboarding System Upgrade",
        "Supply Chain Optimization",
        "5G Network Deployment",
        "Digital Marketing Strategy",
        "Automated Financial Reports",
        "Remote Work Infrastructure",
        "Virtual Reality Training",
        "Predictive Maintenance AI",
        "Cybersecurity Awareness Program",
        "User Experience Redesign",
        "Content Personalization AI",
        "Employee Wellness Program",
        "Zero Trust Security Framework",
        "Automated Invoice Processing",
        "Serverless Computing Migration",
        "Voice Search Optimization",
        "AI-driven Fraud Detection",
        "Multi-cloud Strategy",
        "Data Privacy Compliance",
        "Omnichannel Retail Strategy",
    ]

    descriptions: list[str] = [
        "This project aims to modernize the customer relationship management system by integrating AI-powered analytics.",
        "Our goal is to enhance the user experience and improve conversion rates for the online store platform.",
        "A strategic plan for migrating company assets to cloud infrastructure for scalability and performance.",
        "Implementing advanced cybersecurity measures to protect against emerging threats and vulnerabilities.",
        "Exploring blockchain technology for secure and transparent payment transactions.",
        "Enhancing customer support efficiency through AI-driven automation and chatbots.",
        "Optimizing website SEO strategies to improve visibility and organic traffic.",
        "Transitioning to green energy solutions to reduce the company's carbon footprint.",
        "Developing an IoT-based smart home automation system for energy efficiency.",
        "Creating a data analytics dashboard to provide real-time business insights.",
        "Improving the HR onboarding process by automating employee data collection and training programs.",
        "Streamlining supply chain operations to reduce costs and improve efficiency.",
        "Deploying a 5G network infrastructure for faster and more reliable connectivity.",
        "Developing an omnichannel marketing approach to increase brand engagement and customer loyalty.",
        "Implementing AI-powered financial reporting tools for real-time analytics and decision making.",
        "Enhancing remote work infrastructure with better security and collaboration tools.",
        "Introducing virtual reality training modules for employee skill development.",
        "Using AI for predictive maintenance to prevent downtime in manufacturing processes.",
        "Launching a cybersecurity awareness program to educate employees on best security practices.",
        "Redesigning the user experience for a more intuitive and engaging digital interface.",
        "Leveraging AI to personalize content recommendations for users.",
        "Implementing a wellness program to improve employee satisfaction and productivity.",
        "Developing a Zero Trust security framework to enhance corporate data protection.",
        "Automating invoice processing to reduce manual errors and improve efficiency.",
        "Migrating applications to a serverless architecture for cost savings and scalability.",
        "Optimizing voice search capabilities to improve accessibility and engagement.",
        "Deploying AI-driven fraud detection tools to prevent financial scams.",
        "Developing a multi-cloud strategy to ensure reliability and redundancy.",
        "Ensuring compliance with new data privacy regulations through robust security measures.",
        "Building an integrated omnichannel retail strategy for seamless customer experience.",
    ]
    base_year: int = 2024
    days_between_tasks: int = 10

    def __init__(self, generator):
        super().__init__(generator)

        if len(self.titles) != len(self.descriptions):
            error_message = "Mismatch between task titles and descriptions. Both must have the same length."
            raise ValueError(error_message)

        current_year = datetime.now().year
        if not (1900 <= self.base_year <= current_year):
            error_message = f"Invalid base_year: {self.base_year}. Must be between 1900 and {current_year}."
            raise ValueError(error_message)

        if not isinstance(self.days_between_tasks, int) or self.days_between_tasks <= 0:
            error_message = f"Invalid days_between_tasks: {self.days_between_tasks}. Must be a positive integer."
            raise ValueError(error_message)

    def get_static_value(self, items: list[str], index: int) -> str:
        return items[index % len(items)]

    def get_task_title(self, index: int) -> str:
        return self.get_static_value(self.titles, index)

    def get_task_description(self, index: int) -> str:
        return self.get_static_value(self.descriptions, index)

    def get_task_status(self, task_id: int) -> TaskStatus:
        total_tasks: int = len(self.titles)
        statuses: list[TaskStatus] = list(TaskStatus)

        if total_tasks < len(statuses):
            return TaskStatus.PENDING

        tasks_per_status: int = max(1, total_tasks // len(statuses))
        index: int = min((task_id - 1) // tasks_per_status, len(statuses) - 1)

        return statuses[index]

    def get_task_created_at(self, task_id: int) -> datetime:
        base_date = datetime(self.base_year, 1, 1, tzinfo=UTC)
        return base_date + timedelta(days=task_id * self.days_between_tasks)


fake = Faker()
fake.add_provider(TaskProvider)

tasks_db = [
    {
        "id": i,
        "title": fake.get_task_title(i - 1),
        "description": fake.get_task_description(i - 1),
        "status": fake.get_task_status(i),
        "created_at": fake.get_task_created_at(i),
    }
    for i in range(1, len(TaskProvider.titles) + 1)
]

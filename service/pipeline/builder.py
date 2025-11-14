"""Translation pipeline builder implementing Builder pattern."""

import logging
from typing import Optional

from service.pipeline.handlers.base_handler import TranslationHandler
from service.pipeline.handlers.validation_handler import ValidationHandler
from service.pipeline.handlers.execution_handler import ExecutionHandler
from service.pipeline.handlers.persistence_handler import PersistenceHandler
from service.pipeline.handlers.logging_handler import LoggingHandler

from infrastructure.executors.langgraph_executor import LangGraphExecutor
from infrastructure.repositories.subtitle_repository import SubtitleRepository


class TranslationPipelineBuilder:
    """
    Builds translation processing pipeline using Builder pattern.
    Chains handlers together using Chain of Responsibility pattern.
    """

    def __init__(self):
        """Initialize pipeline builder."""
        self._handlers = []

    def add_validation(self) -> "TranslationPipelineBuilder":
        """
        Add validation handler to pipeline.

        Returns:
            Self for method chaining
        """
        self._handlers.append(ValidationHandler())
        return self

    def add_execution(
        self,
        executor: LangGraphExecutor,
        max_attempts: int = 3,
        logger: Optional[logging.Logger] = None,
    ) -> "TranslationPipelineBuilder":
        """
        Add execution handler to pipeline.

        Args:
            executor: Translation executor instance
            max_attempts: Maximum retry attempts
            logger: Logger instance

        Returns:
            Self for method chaining
        """
        self._handlers.append(ExecutionHandler(executor, max_attempts, logger))
        return self

    def add_persistence(
        self,
        subtitle_repository: SubtitleRepository,
        logger: Optional[logging.Logger] = None,
    ) -> "TranslationPipelineBuilder":
        """
        Add persistence handler to pipeline.

        Args:
            subtitle_repository: Subtitle repository instance
            logger: Logger instance

        Returns:
            Self for method chaining
        """
        self._handlers.append(PersistenceHandler(subtitle_repository, logger))
        return self

    def add_logging(
        self, logger: Optional[logging.Logger] = None
    ) -> "TranslationPipelineBuilder":
        """
        Add logging handler to pipeline.

        Args:
            logger: Logger instance

        Returns:
            Self for method chaining
        """
        self._handlers.append(LoggingHandler(logger))
        return self

    def build(self) -> TranslationHandler:
        """
        Build the pipeline by chaining handlers.

        Returns:
            First handler in the chain

        Raises:
            ValueError: If no handlers were added
        """
        if not self._handlers:
            raise ValueError("Pipeline must have at least one handler")

        # Chain handlers together
        for i in range(len(self._handlers) - 1):
            self._handlers[i].set_next(self._handlers[i + 1])

        # Return first handler
        return self._handlers[0]

    def reset(self) -> "TranslationPipelineBuilder":
        """
        Reset builder to start fresh.

        Returns:
            Self for method chaining
        """
        self._handlers = []
        return self

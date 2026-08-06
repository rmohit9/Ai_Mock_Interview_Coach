import json
import os
from datetime import datetime


class InterviewLogger:

    @staticmethod
    def save(report):

        os.makedirs("logs", exist_ok=True)

        filename = datetime.now().strftime(
            "%Y%m%d_%H%M%S.json"
        )

        path = os.path.join(
            "logs",
            filename,
        )

        with open(path, "w", encoding="utf-8") as f:

            json.dump(
                report,
                f,
                indent=4,
                ensure_ascii=False,
            )

        return path
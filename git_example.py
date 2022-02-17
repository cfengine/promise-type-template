import sys
import os
from cfengine import PromiseModule, ValidationError

# This is an example implementation of the git promise type.
# To make your own promise type, you will need to replace the code
# in validate_promise() and evaluate_promise().

class GitExamplePromiseTypeModule(PromiseModule):
    def validate_promise(self, promiser, attributes):
        if not promiser.startswith("/"):
            raise ValidationError(f"File path '{promiser}' must be absolute")
        for name, value in attributes.items():
            if name != "repository":
                raise ValidationError(f"Unknown attribute '{name}' for git_example promises")
            if name == "repository" and type(value) is not str:
                raise ValidationError(f"'repository' must be string for git_example promises")

    def evaluate_promise(self, promiser, attributes):
        if not promiser.startswith("/"):
            raise ValidationError("File path must be absolute")

        folder = promiser
        url = attributes["repository"]

        if os.path.exists(folder):
            self.promise_kept()
            return

        self.log_info(f"Cloning '{url}' -> '{folder}'...")
        os.system(f"git clone {url} {folder} 1>/dev/null 2>/dev/null")

        if os.path.exists(folder):
            self.log_info(f"Successfully cloned '{url}' -> '{folder}'")
            self.promise_repaired()
        else:
            self.log_error(f"Failed to clone '{url}' -> '{folder}'")
            self.promise_not_kept()


if __name__ == "__main__":
    GitExamplePromiseTypeModule().start()

# Logger
This logger exists to replace boilerplate code for creating loggers. It also uses a custom format.
In future, this package can be extended to include functions that write logs to an elastic search cluster or something too.

**Usage:**  
Convension is to create many loggers, passing __name__ as the name.
Levels should be passed from a config file so that all logger levels are in one place. This allows for much easier debugging.
```
logger(name, level))

Args:
    name (str): name of the logger.
    level (str): name of the logger level. Valid values are "CRITICAL", "ERROR", "WARNING", "INFO", and "DEBUG"

Returns:
    logging.logger obj: A custom logger instance.
```

**Example**
```
from LoraLogger.logger import logger

logger = logger(__name__, LOGGERS.EXAMPLE)
logger.info("This will write if LOGGERS.EXAMPLE is >= INFO")
logger.debug("This will write if LOGGERS.EXAMPLE is >= DEBUG")
```

**Requirements**
```

```


# Contents
```
Package
logger
 ┣ __init__.py
 ┗ logger.py
```

## **logger.py**
Contains the logger function.

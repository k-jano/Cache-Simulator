## Preqrequisities
 - Redis server
 - Modyfied [Hyperflow](https://github.com/k-jano/hyperflow)
 - ``data.json`` file containing a dict with with job parameters, obtaining from [process.py](https://github.com/k-jano/log-parser/blob/master/process.py)
 - ``file_size.json`` file containing a dict with file sizes, obtaining from [file_size.py](https://github.com/k-jano/log-parser/blob/master/file_size.py)
 - ``freq.json`` file containing frequency counter for each file, obtaining from ``utils/freq.py``

## Installation
```
pip install -r requirements.txt
```

## Usage
```
python simulator.py
```

## Config files
Example of config files ``data.json``, ``file_size.json``, ``freq.json`` are already stored in ``data`` directory.
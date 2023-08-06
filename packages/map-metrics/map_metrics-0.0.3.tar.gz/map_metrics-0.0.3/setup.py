# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['map_metrics', 'map_metrics.utils']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5.1,<3.0.0',
 'nptyping>=1.4.4,<2.0.0',
 'numpy>=1.19.5,<2.0.0',
 'open3d>=0.14.1,<0.15.0',
 'scikit-learn>=0.24.2,<0.25.0']

setup_kwargs = {
    'name': 'map-metrics',
    'version': '0.0.3',
    'description': 'Short',
    'long_description': '# map-metrics\nMap metrics toolkit provides a set of metrics **to quantitatively evaluate trajectory quality via estimating\nconsistency of the map aggregated from point clouds**.\n\nGPS or Motion Capture systems are not always available in perception systems, or their quality is not enough (GPS on\nsmall-scale distances) for use as ground truth trajectory. Thus, common full-reference trajectory metrics (APE,\nRPE, and their modifications) could not be applied to evaluate trajectory quality. When 3D sensing technologies (depth\ncamera, LiDAR) are available on the perception system, one can alternatively assess trajectory quality -- estimate\nthe consistency of the map from registered point clouds via the trajectory.\n\n## Installation\n```bash\n$ pip install map-metrics\n```\n\n## Usage\nRun metric algorithms from `map_metrics` on your point cloud data.\n\n```python\nfrom map_metrics.metrics import mme\nfrom map_metrics.config import LidarConfig\n\nresult = mme(pointclouds, poses, config=LidarConfig)\n```\n\n## License\nLicense...\n\n## Credits\nCredits...\n\n## Citation\nIf you use this toolkit or MOM-metric results, please, cite our work:\n\n    @misc{kornilova2021benchmark,\n        title={Be your own Benchmark: No-Reference Trajectory Metric on Registered Point Clouds},\n        author={Anastasiia Kornilova and Gonzalo Ferrer},\n        year={2021},\n        eprint={2106.11351},\n        archivePrefix={arXiv},\n        primaryClass={cs.RO}\n    }\n',
    'author': 'Arthur',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

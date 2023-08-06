__version__ = '0.6.0'
git_version = '66bbbda56d00ac78397709094f611ac1d43a9393'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()

{ lib
, buildPythonPackage
, fetchPypi
, setuptools
, awkward
, uproot
, dask
, dask-awkward
, dask-histogram
, correctionlib
, pyarrow
, fsspec
, matplotlib
, numba
, numpy
, scipy
, tqdm
, lz4
, cloudpickle
, toml
, mplhep
, packaging
, pandas
, hist
, cachetools
}:

buildPythonPackage rec {
  pname = "coffea";
  version = "2023.5.0rc0";

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-MOTea5cepjVx80XG6wZCJychO8VymbaxG4OWsBM3GyI=";
  };

  propagatedBuildInputs = [ awkward uproot dask dask-awkward dask-histogram correctionlib pyarrow fsspec matplotlib numba numpy scipy tqdm lz4 cloudpickle toml mplhep packaging pandas hist cachetools ];

  doCheck = false;
}

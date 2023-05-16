{ lib
, buildPythonPackage
, fetchFromGitHub
, pythonOlder
, boost-histogram
, dask
, hatch-vcs
, hatchling
}:

buildPythonPackage rec {
  pname = "dask-histogram";
  version = "2023.5.0";
  format = "pyproject";

  disabled = pythonOlder "3.8";

  src = fetchFromGitHub {
    owner = "dask-contrib";
    repo = pname;
    rev = version;
    hash = "sha256-cj4izzXPXs6k1SnJTOMhLJQs3tIK69TLQ1TyShUBxfM=";
  };

  nativeBuildInputs = [
    hatch-vcs
    hatchling
  ];

  propagatedBuildInputs = [
    boost-histogram
    dask
  ];

  SETUPTOOLS_SCM_PRETEND_VERSION = version;

  doCheck = false;
}

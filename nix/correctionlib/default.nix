{ lib
, buildPythonPackage
, fetchPypi
, setuptools-scm
, scikit-build
, cmake
, numpy
, pydantic
, rich
}:

buildPythonPackage rec {
  pname = "correctionlib";
  version = "2.2.2";

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-h3eggtPLSF/8ShQ5xzowZW1KSlcI/YBsPu3lsSyzHkw=";
  };

  nativeBuildInputs = [ cmake setuptools-scm scikit-build ];
  propagatedBuildInputs = [ numpy pydantic rich ];

  dontUseCmakeConfigure = true;
  doCheck = false;
}

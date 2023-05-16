{ lib
, buildPythonPackage
, fetchFromGitHub
, setuptools
}:

buildPythonPackage rec {
  pname = "cloudpickle";
  version = "v2.2.1";

  src = fetchFromGitHub {
    owner = "cloudpipe";
    repo = pname;
    rev = version;
    hash = "sha256-Xdk81kuVWesnuPRdStkRcXhsNOw32/Ow21m4bxyUwHU=";
  };

  nativeBuildInputs = [ setuptools ];

  doCheck = false;
}

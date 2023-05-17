{
  description = "HEP machine-learning demos.";

  inputs = {
    root-curated.url = "github:umd-lhcb/root-curated/dev";
    nixpkgs.follows = "root-curated/nixpkgs";
    flake-utils.follows = "root-curated/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, root-curated }:
    {
      overlay = import ./nix/overlay.nix;
    } //
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            root-curated.overlay
            self.overlay
          ];
        };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
      in
      {
        devShell = pkgs.mkShell {
          name = "ml-demo";
          buildInputs = with pythonPackages; [
            tensorflow
            keras
            coffea
            hist
            scikit-learn
          ];
        };
      });
}

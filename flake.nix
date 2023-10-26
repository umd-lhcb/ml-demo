{
  description = "HEP machine-learning demos.";

  inputs = {
    root-curated.url = "github:umd-lhcb/root-curated/dev";
    nixpkgs.follows = "root-curated/nixpkgs";
    flake-utils.follows = "root-curated/flake-utils";
    nixgl.url = "github:guibou/nixGL";
  };

  outputs = { self, nixpkgs, flake-utils, root-curated, nixgl }:
    {
      overlay = import ./nix/overlay.nix;
    } //
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            root-curated.overlay
            nixgl.overlay
            self.overlay
          ];
          config = {
            allowUnfree = true;
          };
        };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
      in
      {
        devShell = pkgs.mkShell {
          name = "ml-demo";
          buildInputs = with pythonPackages; [
            # tensorflow & co
            #tensorflow
            tensorflowWithCuda  # compiles w/ --impure flag?
            #tensorflow-bin
            pkgs.cudatoolkit

            keras
            coffea
            hist
            scikit-learn

            # helpers
            pkgs.nixgl.auto.nixGLDefault
          ];

          shellHook = ''
            # enable cuda support on WSL 2
            export LD_LIBRARY_PATH=/usr/lib/wsl/lib
          '';
        };
      });
}

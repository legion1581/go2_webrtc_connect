{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pkgs.stdenv.cc.cc.lib
            pkgs.hello
            pkgs.python312
            pkgs.python312Packages.pip
            pkgs.python312Packages.setuptools
            pkgs.python312Packages.virtualenv
            pkgs.python312Packages.pyaudio
            pkgs.ffmpeg_6
            pkgs.portaudio
            pkgs.ffmpeg_6.dev
          ];
          shellHook = ''
                      # fixes libstdc++ issues and portaudio issues
                      export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib/:${pkgs.portaudio}/lib/:$LD_LIBRARY_PATH"
                      source env/bin/activate
                      '';
        };

      });
}



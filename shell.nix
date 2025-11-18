{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.git
    pkgs.curl
    pkgs.uv
    pkgs.just
    # add other tools you want
  ];
}

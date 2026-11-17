// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title Registro de Partidas e Vencedores de Torneio (Rocket League)
contract RocketLeagueTorneio {
    address public owner;
    uint256 public totalPartidas;

    struct Partida {
        string arena;
        address vencedor;
        bool finalizada;
    }

    mapping(uint256 => Partida) private partidas;

    event PartidaCriada(uint256 indexed id, string arena);
    event PartidaFinalizada(uint256 indexed id, address indexed vencedor);

    modifier onlyOwner() {
        require(msg.sender == owner, "Apenas owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function criarPartida(string calldata arena) external onlyOwner returns (uint256 id) {
        require(bytes(arena).length > 0, "Arena vazia");

        id = ++totalPartidas;
        partidas[id] = Partida(arena, address(0), false);

        emit PartidaCriada(id, arena);
    }

    function finalizarPartida(uint256 id, address vencedor) external onlyOwner {
        Partida storage partida = partidas[id];
        require(bytes(partida.arena).length > 0, "Partida inexistente");
        require(!partida.finalizada, "Partida ja finalizada");
        require(vencedor != address(0), "Vencedor invalido");

        partida.vencedor = vencedor;
        partida.finalizada = true;

        emit PartidaFinalizada(id, vencedor);
    }

    function consultarPartida(uint256 id)
        external
        view
        returns (string memory arena, address vencedor, bool finalizada)
    {
        Partida memory partida = partidas[id];
        return (partida.arena, partida.vencedor, partida.finalizada);
    }
}


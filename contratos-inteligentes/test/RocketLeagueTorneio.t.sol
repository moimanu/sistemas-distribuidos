// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {RocketLeagueTorneio} from "../src/RocketLeagueTorneio.sol";

interface Vm {
    function prank(address) external;
    function expectRevert(bytes calldata) external;
    function expectEmit(bool, bool, bool, bool) external;
}

contract RocketLeagueTorneioTest {
    Vm private constant vm = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));

    RocketLeagueTorneio private torneio;
    address private constant JOGADOR = address(0xBEEF);
    address private constant INTRUSO = address(0xDEAD);

    event PartidaCriada(uint256 indexed id, string arena);
    event PartidaFinalizada(uint256 indexed id, address indexed vencedor);

    function setUp() public {
        torneio = new RocketLeagueTorneio();
    }

    function testCriarEConsultarPartida() public {
        vm.expectEmit(true, false, false, true);
        emit PartidaCriada(1, "DFH Stadium");

        uint256 id = torneio.criarPartida("DFH Stadium");
        (string memory arena, address vencedor, bool finalizada) = torneio.consultarPartida(id);

        require(id == 1, "ID esperado 1");
        require(keccak256(bytes(arena)) == keccak256("DFH Stadium"), "Arena incorreta");
        require(vencedor == address(0), "Vencedor deve iniciar zerado");
        require(!finalizada, "Partida nao deve iniciar finalizada");
    }

    function testFinalizarPartidaEmiteEvento() public {
        uint256 id = torneio.criarPartida("Mannfield");

        vm.expectEmit(true, true, false, false);
        emit PartidaFinalizada(id, JOGADOR);
        torneio.finalizarPartida(id, JOGADOR);

        (, address vencedor, bool finalizada) = torneio.consultarPartida(id);
        require(vencedor == JOGADOR, "Vencedor incorreto");
        require(finalizada, "Partida deveria estar finalizada");
    }

    function testReverteQuandoNaoOwnerCriaPartida() public {
        vm.prank(INTRUSO);
        vm.expectRevert(bytes("Apenas owner"));
        torneio.criarPartida("Utopia Coliseum");
    }

    function testReverteQuandoArenaVazia() public {
        vm.expectRevert(bytes("Arena vazia"));
        torneio.criarPartida("");
    }

    function testReverteAoFinalizarDuasVezes() public {
        uint256 id = torneio.criarPartida("Neo Tokyo");
        torneio.finalizarPartida(id, JOGADOR);

        vm.expectRevert(bytes("Partida ja finalizada"));
        torneio.finalizarPartida(id, JOGADOR);
    }
}


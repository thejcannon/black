#!/usr/bin/env python3

import asyncio
import unittest
from contextlib import contextmanager
from platform import system
from subprocess import CalledProcessError
from typing import Iterator

from click.testing import CliRunner

from black_primer import cli, lib


@contextmanager
def event_loop() -> Iterator[None]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        yield

    finally:
        loop.close()


class PrimerLibTests(unittest.TestCase):
    @event_loop()
    def test_gen_check_output(self) -> None:
        loop = asyncio.get_event_loop()
        stdout, stderr = loop.run_until_complete(
            lib._gen_check_output(["black", "--help"])
        )
        self.assertTrue("The uncompromising code formatter" in stdout.decode("utf8"))
        self.assertEqual(None, stderr)

        # TODO: Add a test to see failure works on Windows
        if system() == "Windows":
            return

        with self.assertRaises(CalledProcessError):
            loop.run_until_complete(lib._gen_check_output(["/usr/bin/false"]))

    @event_loop()
    def test_process_queue(self) -> None:
        # loop = asyncio.get_event_loop()
        pass


class PrimerCLITests(unittest.TestCase):
    def test_handle_debug(self) -> None:
        self.assertTrue(cli._handle_debug(None, None, True))

    def test_help_output(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli.main, ["--help"])
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()

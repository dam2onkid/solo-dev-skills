#!/usr/bin/env node
import { Command } from "commander";
import { init, add, list } from "../src/commands/init.js";

const program = new Command();

program
  .name("solo-dev-skills")
  .description("CLI tool to initialize solo-dev-skills in your project")
  .version("1.0.0");

program
  .command("init")
  .description("Initialize all skills in your project")
  .option(
    "-e, --environment <env>",
    "Specify environment (cursor|claude|both)",
    "both"
  )
  .action(init);

program
  .command("add <skills...>")
  .description("Add specific skills to your project")
  .option(
    "-e, --environment <env>",
    "Specify environment (cursor|claude|both)",
    "both"
  )
  .action(add);

program.command("list").description("List all available skills").action(list);

program.parse();

import { fileURLToPath } from "url";
import { dirname, join } from "path";
import fs from "fs-extra";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const SKILLS_SOURCE = join(__dirname, "../../.claude/skills");

const TARGETS = {
  cursor: ".cursor/skills",
  claude: ".claude/skills",
};

async function getAvailableSkills() {
  const items = await fs.readdir(SKILLS_SOURCE);
  return items.filter((s) => !s.startsWith("."));
}

function getTargetPaths(environment) {
  if (!["cursor", "claude", "both"].includes(environment)) {
    console.error(
      `Invalid environment: ${environment}. Use cursor, claude, or both.`
    );
    process.exit(1);
  }
  return environment === "both"
    ? Object.values(TARGETS)
    : [TARGETS[environment]];
}

async function copySkills(skillNames, targets) {
  const cwd = process.cwd();
  const available = await getAvailableSkills();

  const invalid = skillNames.filter((s) => !available.includes(s));
  if (invalid.length > 0) {
    console.error(`Unknown skills: ${invalid.join(", ")}`);
    console.error(`Run 'solo-dev-skills list' to see available skills.`);
    process.exit(1);
  }

  for (const target of targets) {
    const targetPath = join(cwd, target);
    await fs.ensureDir(targetPath);

    for (const skill of skillNames) {
      const src = join(SKILLS_SOURCE, skill);
      const dest = join(targetPath, skill);
      await fs.copy(src, dest, { overwrite: true });
      console.log(`✓ Copied ${skill} → ${target}/${skill}`);
    }
  }
}

export async function init(options) {
  const targets = getTargetPaths(options.environment);
  const skills = await getAvailableSkills();
  await copySkills(skills, targets);
  console.log(`\n✓ All skills initialized for ${options.environment}`);
}

export async function add(skills, options) {
  const targets = getTargetPaths(options.environment);
  await copySkills(skills, targets);
  console.log(`\n✓ Added ${skills.length} skill(s) for ${options.environment}`);
}

export async function list() {
  const skills = await getAvailableSkills();
  console.log("Available skills:\n");
  skills.forEach((s) => console.log(`  - ${s}`));
  console.log(`\nTotal: ${skills.length} skills`);
}

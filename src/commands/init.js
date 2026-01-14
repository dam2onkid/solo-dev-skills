import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs-extra';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const SKILLS_SOURCE = join(__dirname, '../../.claude/skills');

const TARGETS = {
  cursor: '.cursor/skills',
  claude: '.claude/skills',
};

export async function init(options) {
  const { environment } = options;
  const cwd = process.cwd();

  if (!['cursor', 'claude', 'both'].includes(environment)) {
    console.error(`Invalid environment: ${environment}. Use cursor, claude, or both.`);
    process.exit(1);
  }

  const targets = environment === 'both' 
    ? Object.values(TARGETS) 
    : [TARGETS[environment]];

  const skills = await fs.readdir(SKILLS_SOURCE);
  const skillDirs = skills.filter(s => !s.startsWith('.'));

  for (const target of targets) {
    const targetPath = join(cwd, target);
    
    try {
      await fs.ensureDir(targetPath);
      
      for (const skill of skillDirs) {
        const src = join(SKILLS_SOURCE, skill);
        const dest = join(targetPath, skill);
        await fs.copy(src, dest, { overwrite: true });
        console.log(`✓ Copied ${skill} → ${target}/${skill}`);
      }
    } catch (err) {
      console.error(`✗ Failed to copy to ${target}: ${err.message}`);
      process.exit(1);
    }
  }

  console.log(`\n✓ Skills initialized for ${environment}`);
}

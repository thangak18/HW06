#!/usr/bin/env node

// Deterministic disclosure-control pass for newly generated Newman evidence.
// It preserves counts, test names, status codes, failure messages, and structure,
// while replacing runtime credentials that Newman serializes into JSON/HTML.

const fs = require('fs');

function sanitizeString(value) {
  return value
    .replace(/eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/g, '<REDACTED_JWT>')
    .replace(/Bearer\s+(?!\{\{)[A-Za-z0-9._~+\/-]+/gi, 'Bearer <REDACTED>')
    .replace(/((?:"|&quot;)?(?:password|token|reset_token|authorization|cookie|secret)(?:"|&quot;)?\s*[:=]\s*(?:"|&quot;))[^"<&]*("|&quot;)/gi, '$1<REDACTED>$2')
    .replace(/(password=)[^&\s<"']+/gi, '$1<REDACTED>');
}

function sanitizeValue(value, key = '') {
  const normalizedKey = key.toLowerCase();
  if (/(authorization|password|token|cookie|secret)/.test(normalizedKey)) {
    if (typeof value === 'string') {
      if (value.includes('{{')) return value;
      if (/^Bearer\s+/i.test(value)) return 'Bearer <REDACTED>';
      return '<REDACTED>';
    }
  }
  if (typeof value === 'string') return sanitizeString(value);
  if (Array.isArray(value)) return value.map((entry) => sanitizeValue(entry));
  if (value && typeof value === 'object') {
    for (const [childKey, childValue] of Object.entries(value)) {
      value[childKey] = sanitizeValue(childValue, childKey);
    }
  }
  return value;
}

function main() {
  const [mode, inputPath, outputPath] = process.argv.slice(2);
  if (!['json', 'html'].includes(mode) || !inputPath || !outputPath) {
    throw new Error('Usage: redact_newman_secrets.js <json|html> <input> <output>');
  }
  const raw = fs.readFileSync(inputPath, 'utf8');
  if (mode === 'json') {
    const parsed = JSON.parse(raw);
    fs.writeFileSync(outputPath, `${JSON.stringify(sanitizeValue(parsed), null, 2)}\n`);
  } else {
    fs.writeFileSync(outputPath, sanitizeString(raw));
  }
}

main();

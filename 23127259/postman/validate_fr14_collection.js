#!/usr/bin/env node
/**
 * FR14 Postman Collection Static Validator
 * Validates structural integrity of FR14_Category_CRUD.postman_collection.json
 * Student: 23127259 - Nguyễn Tấn Thắng
 */

const fs = require('fs');
const path = require('path');

const COLLECTION_PATH = path.join(__dirname, 'collections', 'FR14_Category_CRUD.postman_collection.json');

function validate() {
    console.log('=== FR14 Postman Collection Static Validation ===\n');
    
    // 1. Parse JSON
    let collection;
    try {
        const raw = fs.readFileSync(COLLECTION_PATH, 'utf8');
        collection = JSON.parse(raw);
        console.log('✅ PASS: Collection JSON is valid and parseable');
    } catch (e) {
        console.error('❌ FAIL: Collection JSON parse error:', e.message);
        process.exit(1);
    }

    // 2. Validate info block
    const info = collection.info;
    if (!info || !info.name || !info.schema) {
        console.error('❌ FAIL: Missing info.name or info.schema');
        process.exit(1);
    }
    console.log(`✅ PASS: Collection name = "${info.name}"`);
    console.log(`✅ PASS: Schema = ${info.schema}`);

    // 3. Validate collection-level pre-request script (X-Student-Id)
    const collEvent = collection.event || [];
    const preReqScript = collEvent.find(e => e.listen === 'prerequest');
    if (preReqScript) {
        const scriptContent = preReqScript.script.exec.join('\n');
        if (scriptContent.includes('X-Student-Id') && scriptContent.includes('23127259')) {
            console.log('✅ PASS: Collection-level pre-request injects X-Student-Id: 23127259');
        } else {
            console.error('❌ FAIL: Collection pre-request script missing X-Student-Id injection');
        }
    } else {
        console.error('❌ FAIL: No collection-level pre-request script found');
    }

    // 4. Count requests recursively
    let totalRequests = 0;
    let totalTests = 0;
    let requestsWithStudentId = 0;
    let requestsWithAuth = 0;
    let folders = [];
    let requestNames = [];
    
    function walkItems(items, folderPath) {
        items.forEach(item => {
            if (item.item) {
                // It's a folder
                folders.push(item.name);
                walkItems(item.item, folderPath + '/' + item.name);
            } else if (item.request) {
                totalRequests++;
                requestNames.push(item.name);
                
                // Check for X-Student-Id header
                const headers = item.request.header || [];
                const hasStudentId = headers.some(h => h.key === 'X-Student-Id');
                if (hasStudentId) requestsWithStudentId++;
                
                // Check for Authorization header
                const hasAuth = headers.some(h => h.key === 'Authorization');
                if (hasAuth) requestsWithAuth++;
                
                // Count test assertions
                const events = item.event || [];
                const testEvents = events.filter(e => e.listen === 'test');
                testEvents.forEach(te => {
                    const testContent = te.script.exec.join('\n');
                    const matches = testContent.match(/pm\.test\(/g);
                    if (matches) totalTests += matches.length;
                });
            }
        });
    }

    walkItems(collection.item || [], '');

    console.log(`\n=== Structure Summary ===`);
    console.log(`📁 Folders: ${folders.length}`);
    console.log(`📋 Total Requests: ${totalRequests}`);
    console.log(`🧪 Total pm.test() assertions: ${totalTests}`);
    console.log(`🔑 Requests with X-Student-Id header: ${requestsWithStudentId}/${totalRequests}`);
    console.log(`🔐 Requests with Authorization header: ${requestsWithAuth}/${totalRequests}`);

    // 5. Validate minimum test cases
    // Excluding helpers (3), we need >= 49 test request items
    const helpers = requestNames.filter(n => n.startsWith('HELPER'));
    const testCases = requestNames.filter(n => n.startsWith('TC-FR14'));
    console.log(`\n📊 Helpers: ${helpers.length}`);
    console.log(`📊 Test Cases (TC-FR14-*): ${testCases.length}`);
    
    if (testCases.length >= 42) {
        console.log(`✅ PASS: Meets ≥42 AI-generated test case minimum (actual: ${testCases.length})`);
    } else {
        console.error(`❌ FAIL: Only ${testCases.length} test cases found (need ≥42)`);
    }

    // 6. Check for required test dimensions
    const dimensions = {
        'Happy Path': requestNames.filter(n => /TC-FR14-00[1-6]/.test(n)),
        'Authentication (SEC-01)': requestNames.filter(n => /TC-FR14-0(07|08|09|10|11)/.test(n)),
        'Authorization (SEC-02)': requestNames.filter(n => /TC-FR14-01[2-5]/.test(n)),
        'Input Validation (Name)': requestNames.filter(n => /TC-FR14-0(1[6-9]|2[0-3])/.test(n)),
        'Input Validation (ID)': requestNames.filter(n => /TC-FR14-02[4-8]/.test(n)),
        'Security Probes': requestNames.filter(n => /TC-FR14-0(29|30|31|32|33|34)/.test(n)),
        'State Transitions': requestNames.filter(n => /TC-FR14-03[5-8]/.test(n)),
        'Schema Validation': requestNames.filter(n => /TC-FR14-03[9]|TC-FR14-04[0-2]/.test(n)),
        'Human Extension': requestNames.filter(n => /TC-FR14-H/.test(n))
    };

    console.log('\n=== Dimension Coverage ===');
    Object.entries(dimensions).forEach(([dim, cases]) => {
        const status = cases.length > 0 ? '✅' : '❌';
        console.log(`${status} ${dim}: ${cases.length} cases`);
    });

    // 7. Validate all variables are defined
    const vars = collection.variable || [];
    const varNames = vars.map(v => v.key);
    const requiredVars = ['baseUrl', 'studentId', 'adminToken', 'userToken', 'adminEmail', 'adminPassword'];
    console.log('\n=== Variable Validation ===');
    requiredVars.forEach(v => {
        if (varNames.includes(v)) {
            console.log(`✅ Variable "${v}" defined`);
        } else {
            console.error(`❌ Variable "${v}" MISSING`);
        }
    });

    // 8. Folder listing
    console.log('\n=== Folder Structure ===');
    folders.forEach(f => console.log(`  📁 ${f}`));

    console.log('\n=== Validation Complete ===');
}

validate();

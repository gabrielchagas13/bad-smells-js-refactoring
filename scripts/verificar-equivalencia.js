import assert from 'node:assert/strict';
import { ReportGenerator as Original } from '../src/ReportGenerator.js';
import { ReportGenerator as Refactored } from '../src/ReportGenerator.refactored.js';
let count = 0;
for (const role of ['ADMIN', 'USER', 'OTHER']) {
  for (const type of ['CSV', 'HTML', 'INVALID']) {
    for (const value of [0, 499, 500, 501, 1000, 1001]) {
      for (const priority of [undefined, false, true]) {
        const originalItems = [{ id: 1, name: 'A', value, priority }];
        const refactoredItems = structuredClone(originalItems);
        const user = { name: 'U', role };
        const original = new Original({}).generateReport(type, user, originalItems);
        const refactored = new Refactored({}).generateReport(type, user, refactoredItems);
        assert.equal(refactored, original.replaceAll('<tr >', '<tr>'));
        assert.deepEqual(refactoredItems, originalItems);
        count++;
      }
    }
  }
}
console.log(`${count} cenários equivalentes, normalizando somente <tr > para <tr>; mutações preservadas.`);

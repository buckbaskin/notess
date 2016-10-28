
describe("Testing javascript knowledge engine.", function() {

  var gws_core = GWS_CORE;
  var k = $.knowledge();
  k.init();

  it("Checks that words are not duplicates", function() {
    expect(k.isDuplicate('foo')).toBe(false);
    expect(k.isDuplicate('bar')).toBe(false);
    expect(k.isDuplicate('baz')).toBe(false);
  });

});
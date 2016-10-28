
describe("Testing javascript gwscore.", function() {

  it("Test getKeywords and setKeywords w/ many keywords", function() {
    //Full keywords array
    var wordArray = ['word1', 'word2', 'word3'];
    GWS_CORE.setKeywords(wordArray);
    receivedWordArray = GWS_CORE.getKeywords();
    expect(wordArray).toEqual(receivedWordArray);
  });

  it("Test getKeywords and setKeywords w/ no keywords", function() {
    //Empty keywords array
    var wordArray = [];
    GWS_CORE.setKeywords(wordArray);
    var receivedWordArray = GWS_CORE.getKeywords();
    expect(wordArray).toEqual(receivedWordArray);
  });

  it("Test setKeywords w/ already set keywords", function() {
    //Empty keywords array
    var wordArray = ['test1', 'test2'];
    GWS_CORE.setKeywords(wordArray);
    var wordArray2 = ['newtest1', 'newtest2'];
    GWS_CORE.setKeywords(wordArray2);
    var receivedWordArray = GWS_CORE.getKeywords();
    expect(wordArray2).toEqual(receivedWordArray);
  });

  it("Test addKeywords, adding 1 keyword", function() {
    //Empty keywords array
    GWS_CORE.setKeywords(['word1', 'word2', 'word3']);
    GWS_CORE.addKeywords(['word4']);
    receivedWordArray = GWS_CORE.getKeywords()
    expect(receivedWordArray).toEqual(['word1', 'word2', 'word3', 'word4']);
  });

  it("Test addKeywords, adding multiple keywords", function() {
    //Empty keywords array
    GWS_CORE.setKeywords(['word1', 'word2', 'word3']);
    GWS_CORE.addKeywords(['word4', 'word5', 'word6']);
    receivedWordArray = GWS_CORE.getKeywords()
    expect(receivedWordArray).toEqual(['word1', 'word2', 'word3', 'word4', 'word5', 'word6']);
  });
  
});
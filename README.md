# LinkedIn Profile Parser

This is a smaller yet valuable part of the system. An agent uses the parser’s output to extract client details by key. If the initial key doesn’t provide enough information, the agent checks other available keys (e.g., education, userInfo) until it gathers all necessary details for the action (ReAct agent).


I had limited time to work on this but am satisfied with my contribution. The parser is flexible—key names are not hardcoded; available keys are shared at runtime. While field names can vary, meaningful names that clearly describe the data are prioritized for better output quality.

## How to run

1. i also added a bare minimum streamlit application so you can appload a sample linkedin profile pdf and see its response just run

```bash
streamlit run main.py
```

2. check `SpacyLayout.ipynb` for better understanding

## Resources

* https://medium.com/@cerenkaya07/how-to-build-an-nlp-powered-job-matcher-using-my-own-linkedin-profile-bf00fb4bed29

* https://stackoverflow.com/questions/59444065/differentiate-between-countries-and-cities-in-spacy-ner/68345017#68345017

* https://stackoverflow.com/questions/52686159/how-to-extract-the-location-name-country-name-city-name-tourist-places-by-usi

## Future

- Integrate NER for more flexible parsing.
- Improve handling of incomplete or ambiguous data.
- Provide detailed parsing logs for debugging.
- https://medium.com/data-science-collective/how-agents-are-helping-me-find-my-next-job-a-true-story-5af543e048f1


## Credits

- Big thanks to [@ckakgun](https://github.com/ckakgun) for sparking the idea to start with LinkedIn.

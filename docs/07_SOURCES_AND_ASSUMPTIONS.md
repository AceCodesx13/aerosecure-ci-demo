# 7. Sources and simulation assumptions

Prepared October 11, 2026 for the capstone starter. Source links identify real aircraft names/families and documented AWS behavior. They do not validate the synthetic orders or part associations.

## Aircraft identities

- [Airbus passenger aircraft families](https://www.airbus.com/en/products-services/commercial-aircraft/passenger-aircraft)
- [Airbus commercial aircraft presentation](https://www.airbus.com/sites/g/files/jlcbta136/files/2023-12/Airbus-Commercial-corporate-presentation-December-2023.pdf)
- [Boeing 737 Next Generation](https://www.boeing.com/commercial/737ng)
- [Boeing 737 MAX](https://www.boeing.com/Commercial/737MAX)
- [Boeing 777](https://www.boeing.com/commercial/777)
- [Boeing 787](https://www.boeing.com/commercial/787)
- [Embraer orders and deliveries](https://embraer.com/orders-and-deliveries/)
- [Embraer E195 and E-Jets family](https://embraer.com/e-jets/e195/en/)
- [Embraer commercial aviation](https://www.embraer.com/commercial-aviation)
- [ATR aircraft history and model identities](https://www.atr-aircraft.com/about-us/who-we-are/)
- [De Havilland Dash 8 family history](https://dehavilland.com/lvas/)

Aircraft categories are broad teaching categories. Manufacturer attribution uses the familiar aircraft-family brand, not a legal claim about every historical production entity. No performance specifications or operational parts lists were copied.

## AWS behavior

- [SageMaker AI model training](https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-training.html)
- [Custom training containers](https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-training-algo.html)
- [How SageMaker runs a training container](https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-training-algo-running-container.html)
- [SageMaker training storage paths](https://docs.aws.amazon.com/sagemaker/latest/dg/model-train-storage-env-var-summary.html)
- [SageMaker execution roles](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html)
- [S3 Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)
- [AWS ECR registry authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html)

## Project scope

The local capstone fall/spring plan and instructor direction define the fall goal: a trained and evaluated supplier lead-time model connected to deterministic maintenance calculations and fictional shipment rules, with reproducible integrated lab evidence in December. This starter supports that work but does not complete the full integrated application.

## Chosen synthetic assumptions

- 20 models, 20 illustrative categories per model, 16 common items plus 4 major assemblies.
- 50 completed orders per association, totaling 20,000.
- Nine fictional suppliers and three fictional regions.
- Calendar-day target and clean, full-quantity completed receipts.
- Independent data-access and shipment labels with the proposed classroom role/destination matrix.
- Training quote noise, stock/backlog effects, condition effects and random disruptions.
- Chronological cutoffs and label-maturity filtering rather than a random split.
- Approved fictional training derivative for all course participants.

None of the generator's numerical coefficients, supplier behaviors, region rules, maintenance intervals or part numbers are real operational measurements. No conclusions about actual aircraft reliability, real shipment legality or supplier performance follow from this dataset.

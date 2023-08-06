"""
This module contains methods and classes that facilitate evaluation of different types of models. The suggested
workflow for evaluation is to use these higher-level functionalities instead of instantiating
the evaluation classes directly.
"""
# TODO: provide a notebook (and possibly an rst file) that illustrates standard evaluation scenarios and at the same
#  time serves as an integration test

import logging
from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any, Union, Generic, TypeVar, Optional, Sequence, Callable

import matplotlib.figure
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .crossval import VectorModelCrossValidationData, VectorRegressionModelCrossValidationData, \
    VectorClassificationModelCrossValidationData, \
    VectorClassificationModelCrossValidator, VectorRegressionModelCrossValidator, VectorModelCrossValidator, VectorModelCrossValidatorParams
from .eval_stats.eval_stats_base import EvalStats, EvalStatsCollection
from .eval_stats.eval_stats_classification import ClassificationEvalStats
from .eval_stats.eval_stats_regression import RegressionEvalStats
from .evaluator import VectorModelEvaluator, VectorModelEvaluationData, VectorRegressionModelEvaluator, \
    VectorRegressionModelEvaluationData, VectorClassificationModelEvaluator, VectorClassificationModelEvaluationData, \
    VectorRegressionModelEvaluatorParams, VectorClassificationModelEvaluatorParams, VectorModelEvaluatorParams
from ..data import InputOutputData
from ..util.io import ResultWriter
from ..util.string import prettyStringRepr
from ..vector_model import VectorClassificationModel, VectorRegressionModel, VectorModel

log = logging.getLogger(__name__)

TModel = TypeVar("TModel", bound=VectorModel)
TEvalStats = TypeVar("TEvalStats", bound=EvalStats)
TEvalStatsCollection = TypeVar("TEvalStatsCollection", bound=EvalStatsCollection)
TEvaluator = TypeVar("TEvaluator", bound=VectorModelEvaluator)
TCrossValidator = TypeVar("TCrossValidator", bound=VectorModelCrossValidator)
TEvalData = TypeVar("TEvalData", bound=VectorModelEvaluationData)
TCrossValData = TypeVar("TCrossValData", bound=VectorModelCrossValidationData)


def _isRegression(model: Optional[VectorModel], isRegression: Optional[bool]) -> bool:
    if model is None and isRegression is None or (model is not None and isRegression is not None):
        raise ValueError("One of the two parameters have to be passed: model or isRegression")

    if isRegression is None:
        model: VectorModel
        return model.isRegressionModel()
    return isRegression


def createVectorModelEvaluator(data: InputOutputData, model: VectorModel = None,
        isRegression: bool = None, params: Union[VectorModelEvaluatorParams, Dict[str, Any]] = None, **kwargs) \
            -> Union[VectorRegressionModelEvaluator, VectorClassificationModelEvaluator]:
    if params is not None and len(kwargs) > 0:
        raise ValueError("Provide either params or keyword arguments")
    if params is None:
        params = kwargs
    regression = _isRegression(model, isRegression)
    if regression:
        params = VectorRegressionModelEvaluatorParams.fromDictOrInstance(params)
    else:
        params = VectorClassificationModelEvaluatorParams.fromDictOrInstance(params)
    cons = VectorRegressionModelEvaluator if regression else VectorClassificationModelEvaluator
    return cons(data, params=params)


def createVectorModelCrossValidator(data: InputOutputData, model: VectorModel = None,
        isRegression: bool = None,
        params: Union[VectorModelCrossValidatorParams, Dict[str, Any]] = None,
        **kwArgsOldParams) -> Union[VectorClassificationModelCrossValidator, VectorRegressionModelCrossValidator]:
    if params is not None:
        params = VectorModelCrossValidatorParams.fromDictOrInstance(params)
    params = VectorModelCrossValidatorParams.fromEitherDictOrInstance(kwArgsOldParams, params)
    cons = VectorRegressionModelCrossValidator if _isRegression(model, isRegression) else VectorClassificationModelCrossValidator
    return cons(data, params=params)


def createEvaluationUtil(data: InputOutputData, model: VectorModel = None, isRegression: bool = None,
        evaluatorParams: Optional[Dict[str, Any]] = None,
        crossValidatorParams: Optional[Dict[str, Any]] = None) \
            -> Union["ClassificationEvaluationUtil", "RegressionEvaluationUtil"]:
    cons = RegressionEvaluationUtil if _isRegression(model, isRegression) else ClassificationEvaluationUtil
    return cons(data, evaluatorParams=evaluatorParams, crossValidatorParams=crossValidatorParams)


def evalModelViaEvaluator(model: TModel, inputOutputData: InputOutputData, testFraction=0.2,
        plotTargetDistribution=False, computeProbabilities=True, normalizePlots=True, randomSeed=60) -> TEvalData:
    """
    Evaluates the given model via a simple evaluation mechanism that uses a single split

    :param model: the model to evaluate
    :param inputOutputData: data on which to evaluate
    :param testFraction: the fraction of the data to test on
    :param plotTargetDistribution: whether to plot the target values distribution in the entire dataset
    :param computeProbabilities: only relevant if the model is a classifier
    :param normalizePlots: whether to normalize plotted distributions such that the sum/integrate to 1
    :param randomSeed:

    :return: the evaluation data
    """
    if plotTargetDistribution:
        title = "Distribution of target values in entire dataset"
        fig = plt.figure(title)

        outputDistributionSeries = inputOutputData.outputs.iloc[:, 0]
        log.info(f"Description of target column in training set: \n{outputDistributionSeries.describe()}")
        if not model.isRegressionModel():
            outputDistributionSeries = outputDistributionSeries.value_counts(normalize=normalizePlots)
            ax = sns.barplot(outputDistributionSeries.index, outputDistributionSeries.values)
            ax.set_ylabel("%")
        else:
            ax = sns.distplot(outputDistributionSeries)
            ax.set_ylabel("Probability density")
        ax.set_title(title)
        ax.set_xlabel("target value")
        fig.show()

    if model.isRegressionModel():
        evaluatorParams = dict(testFraction=testFraction, randomSeed=randomSeed)
    else:
        evaluatorParams = dict(testFraction=testFraction, computeProbabilities=computeProbabilities, randomSeed=randomSeed)
    ev = createEvaluationUtil(inputOutputData, model=model, evaluatorParams=evaluatorParams)
    return ev.performSimpleEvaluation(model, showPlots=True, logResults=True)


class EvaluationUtil(ABC, Generic[TModel, TEvaluator, TEvalData, TCrossValidator, TCrossValData, TEvalStats]):
    """
    Utility class for the evaluation of models based on a dataset
    """
    def __init__(self, inputOutputData: InputOutputData,
            evaluatorParams: Optional[Union[VectorRegressionModelEvaluatorParams, VectorClassificationModelEvaluatorParams, Dict[str, Any]]] = None,
            crossValidatorParams: Optional[Union[VectorModelCrossValidatorParams, Dict[str, Any]]] = None):
        """
        :param inputOutputData: the data set to use for evaluation
        :param evaluatorParams: parameters with which to instantiate evaluators
        :param crossValidatorParams: parameters with which to instantiate cross-validators
        """
        if evaluatorParams is None:
            evaluatorParams = dict(testFraction=0.2)
        if crossValidatorParams is None:
            crossValidatorParams = VectorModelCrossValidatorParams(folds=5)
        self.evaluatorParams = evaluatorParams
        self.crossValidatorParams = crossValidatorParams
        self.inputOutputData = inputOutputData

    class ResultCollector:
        def __init__(self, showPlots: bool = True, resultWriter: Optional[ResultWriter] = None):
            self.showPlots = showPlots
            self.resultWriter = resultWriter

        def addFigure(self, name, fig: matplotlib.figure.Figure):
            if self.resultWriter is not None:
                self.resultWriter.writeFigure(name, fig, closeFigure=not self.showPlots)

        def child(self, addedFilenamePrefix):
            resultWriter = self.resultWriter
            if resultWriter:
                resultWriter = resultWriter.childWithAddedPrefix(addedFilenamePrefix)
            return self.__class__(showPlots=self.showPlots, resultWriter=resultWriter)

    def createEvaluator(self, model: TModel = None, isRegression: bool = None) -> TEvaluator:
        """
        Creates an evaluator holding the current input-output data

        :param model: the model for which to create an evaluator (just for reading off regression or classification,
            the resulting evaluator will work on other models as well)
        :param isRegression: whether to create a regression model evaluator. Either this or model have to be specified
        :return: an evaluator
        """
        return createVectorModelEvaluator(self.inputOutputData, model=model, isRegression=isRegression, params=self.evaluatorParams)

    def createCrossValidator(self, model: TModel = None, isRegression: bool = None) -> TCrossValidator:
        """
        Creates a cross-validator holding the current input-output data

        :param model: the model for which to create a cross-validator (just for reading off regression or classification,
            the resulting evaluator will work on other models as well)
        :param isRegression: whether to create a regression model cross-validator. Either this or model have to be specified
        :return: an evaluator
        """
        return createVectorModelCrossValidator(self.inputOutputData, model=model, isRegression=isRegression, params=self.crossValidatorParams)

    def performSimpleEvaluation(self, model: TModel, createPlots=True, showPlots=False, logResults=True, resultWriter: ResultWriter = None,
            additionalEvaluationOnTrainingData=False, fitModel=True, writeEvalStats=False) -> TEvalData:
        if showPlots and not createPlots:
            raise ValueError("showPlots=True requires createPlots=True")
        resultWriter = self._resultWriterForModel(resultWriter, model)
        evaluator = self.createEvaluator(model)
        log.info(f"Evaluating {model} via {evaluator}")
        if fitModel:
            evaluator.fitModel(model)

        def gatherResults(evalResultData: VectorModelEvaluationData, resultWriter, subtitlePrefix=""):
            strEvalResults = ""
            for predictedVarName in evalResultData.predictedVarNames:
                evalStats = evalResultData.getEvalStats(predictedVarName)
                strEvalResult = str(evalStats)
                if logResults:
                    log.info(f"{subtitlePrefix}Evaluation results for {predictedVarName}: {strEvalResult}")
                strEvalResults += predictedVarName + ": " + strEvalResult + "\n"
                if writeEvalStats and resultWriter is not None:
                    resultWriter.writePickle(f"eval-stats-{predictedVarName}", evalStats)
            strEvalResults += f"\n\n{prettyStringRepr(model)}"
            if resultWriter is not None:
                resultWriter.writeTextFile("evaluator-results", strEvalResults)
            if createPlots:
                self.createPlots(evalResultData, showPlots=showPlots, resultWriter=resultWriter, subtitlePrefix=subtitlePrefix)

        evalResultData = evaluator.evalModel(model)
        gatherResults(evalResultData, resultWriter)
        if additionalEvaluationOnTrainingData:
            evalResultDataTrain = evaluator.evalModel(model, onTrainingData=True)
            additionalResultWriter = resultWriter.childWithAddedPrefix("onTrain-") if resultWriter is not None else None
            gatherResults(evalResultDataTrain, additionalResultWriter, subtitlePrefix="[onTrain] ")

        return evalResultData

    @staticmethod
    def _resultWriterForModel(resultWriter: Optional[ResultWriter], model: TModel) -> Optional[ResultWriter]:
        if resultWriter is None:
            return None
        return resultWriter.childWithAddedPrefix(model.getName() + "-")

    def performCrossValidation(self, model: TModel, showPlots=False, logResults=True, resultWriter: Optional[ResultWriter] = None) -> TCrossValData:
        """
        Evaluates the given model via cross-validation

        :param model: the model to evaluate
        :param showPlots: whether to show plots that visualise evaluation results (combining all folds)
        :param logResults: whether to log evaluation results
        :param resultWriter: a writer with which to store text files and plots. The evaluated model's name is added to each filename
            automatically
        :return: cross-validation result data
        """
        resultWriter = self._resultWriterForModel(resultWriter, model)
        crossValidator = self.createCrossValidator(model)
        crossValidationData = crossValidator.evalModel(model)
        aggStatsByVar = {varName: crossValidationData.getEvalStatsCollection(predictedVarName=varName).aggStats()
                for varName in crossValidationData.predictedVarNames}
        strEvalResults = str(pd.DataFrame.from_dict(aggStatsByVar, orient="index"))
        if logResults:
            log.info(f"Cross-validation results:\n{strEvalResults}")
        if resultWriter is not None:
            resultWriter.writeTextFile("crossval-results", strEvalResults)
        self.createPlots(crossValidationData, showPlots=showPlots, resultWriter=resultWriter)
        return crossValidationData

    def compareModels(self, models: Sequence[TModel], resultWriter: Optional[ResultWriter] = None, useCrossValidation=False,
            fitModels=True, writeIndividualResults=True, sortColumn: Optional[str] = None, sortAscending: bool = True) -> pd.DataFrame:
        """
        Compares several models via simple evaluation or cross-validation

        :param models: the models to compare
        :param resultWriter: a writer with which to store results of the comparison
        :param useCrossValidation: whether to use cross-validation in order to evaluate models; if False, use a simple evaluation
            on test data (single split)
        :param fitModels: whether to fit models before evaluating them; this can only be False if useCrossValidation=False
        :param writeIndividualResults: whether to write results files on each individual model (in addition to the comparison
            summary)
        :param sortColumn: column/metric name by which to sort
        :param sortAscending: whether to sort in ascending order
        :return: a data frame containing evaluation metrics on all models
        """
        statsList = []
        for model in models:
            if useCrossValidation:
                if not fitModels:
                    raise ValueError("Cross-validation necessitates that models be retrained; got fitModels=False")
                crossValidationResult = self.performCrossValidation(model, resultWriter=resultWriter if writeIndividualResults else None)
                statsDict = crossValidationResult.getEvalStatsCollection().aggStats()
            else:
                evalStats: EvalStats = self.performSimpleEvaluation(model, resultWriter=resultWriter if writeIndividualResults else None,
                    fitModel=fitModels).getEvalStats()
                statsDict = evalStats.getAll()
            statsDict["modelName"] = model.getName()
            statsList.append(statsDict)
        resultsDF = pd.DataFrame(statsList).set_index("modelName")
        if sortColumn is not None:
            if sortColumn not in resultsDF.columns:
                log.warning(f"Requested sort column '{sortColumn}' not in list of columns {list(resultsDF.columns)}")
            else:
                resultsDF.sort_values(sortColumn, ascending=sortAscending, inplace=True)
        strResults = f"Model comparison results:\n{resultsDF.to_string()}"
        log.info(strResults)
        if resultWriter is not None:
            suffix = "crossval" if useCrossValidation else "simple-eval"
            strResults += "\n\n" + "\n\n".join([f"{model.getName()} = {str(model)}" for model in models])
            resultWriter.writeTextFile(f"model-comparison-results-{suffix}", strResults)
        return resultsDF

    def compareModelsCrossValidation(self, models: Sequence[TModel], resultWriter: Optional[ResultWriter] = None) -> pd.DataFrame:
        """
        Compares several models via cross-validation

        :param models: the models to compare
        :param resultWriter: a writer with which to store results of the comparison
        :return: a data frame containing evaluation metrics on all models
        """
        return self.compareModels(models, resultWriter=resultWriter, useCrossValidation=True)

    def createPlots(self, data: Union[TEvalData, TCrossValData], showPlots=True, resultWriter: Optional[ResultWriter] = None, subtitlePrefix: str = ""):
        """
        Creates default plots that visualise the results in the given evaluation data

        :param data: the evaluation data for which to create the default plots
        :param showPlots: whether to show plots
        :param resultWriter: if not None, plots will be written using this writer
        :param subtitlePrefix: a prefix to add to the subtitle (which itself is the model name)
        """
        if not showPlots and resultWriter is None:
            return
        resultCollector = self.ResultCollector(showPlots=showPlots, resultWriter=resultWriter)
        self._createPlots(data, resultCollector, subtitle=subtitlePrefix + data.modelName)

    def _createPlots(self, data: Union[TEvalData, TCrossValData], resultCollector: ResultCollector, subtitle=None):

        def createPlots(predVarName, rc, subt):
            if isinstance(data, VectorModelCrossValidationData):
                evalStats = data.getEvalStatsCollection(predictedVarName=predVarName).getGlobalStats()
            elif isinstance(data, VectorModelEvaluationData):
                evalStats = data.getEvalStats(predictedVarName=predVarName)
            else:
                raise ValueError(f"Unexpected argument: data={data}")
            return self._createEvalStatsPlots(evalStats, rc, subtitle=subt)

        predictedVarNames = data.predictedVarNames
        if len(predictedVarNames) == 1:
            createPlots(predictedVarNames[0], resultCollector, subtitle)
        else:
            for predictedVarName in predictedVarNames:
                createPlots(predictedVarName, resultCollector.child(predictedVarName+"-"), f"{predictedVarName}, {subtitle}")

    @abstractmethod
    def _createEvalStatsPlots(self, evalStats: TEvalStats, resultCollector: ResultCollector, subtitle=None):
        """
        :param evalStats: the evaluation results for which to create plots
        :param resultCollector: the collector to which all plots are to be passed
        :param subtitle: the subtitle to use for generated plots (if any)
        """
        pass


class RegressionEvaluationUtil(EvaluationUtil[VectorRegressionModel, VectorRegressionModelEvaluator, VectorRegressionModelEvaluationData, VectorRegressionModelCrossValidator, VectorRegressionModelCrossValidationData, RegressionEvalStats]):
    def _createEvalStatsPlots(self, evalStats: RegressionEvalStats, resultCollector: EvaluationUtil.ResultCollector, subtitle=None):
        resultCollector.addFigure("error-dist", evalStats.plotErrorDistribution(titleAdd=subtitle))
        resultCollector.addFigure("heatmap-gt-pred", evalStats.plotHeatmapGroundTruthPredictions(titleAdd=subtitle))
        resultCollector.addFigure("scatter-gt-pred", evalStats.plotScatterGroundTruthPredictions(titleAdd=subtitle))


class ClassificationEvaluationUtil(EvaluationUtil[VectorClassificationModel, VectorClassificationModelEvaluator, VectorClassificationModelEvaluationData, VectorClassificationModelCrossValidator, VectorClassificationModelCrossValidationData, ClassificationEvalStats]):
    def _createEvalStatsPlots(self, evalStats: ClassificationEvalStats, resultCollector: EvaluationUtil.ResultCollector, subtitle=None):
        resultCollector.addFigure("confusion-matrix", evalStats.plotConfusionMatrix(titleAdd=subtitle))


class MultiDataEvaluationUtil:
    def __init__(self, inputOutputDataDict: Dict[str, InputOutputData], keyName: str = "dataset"):
        """
        :param inputOutputDataDict: a dictionary mapping from names to the data sets with which to evaluate models
        :param keyName: a name for the key value used in inputOutputDataDict
        """
        self.inputOutputDataDict = inputOutputDataDict
        self.keyName = keyName

    def compareModelsCrossValidation(self, modelFactories: Sequence[Callable[[], VectorModel]],
            resultWriter: Optional[ResultWriter] = None, writePerDatasetResults=True,
            crossValidatorParams: Optional[Dict[str, Any]] = None, columnNameForModelRanking: str = None, rankMax=True) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        :param modelFactories: a sequence of factory functions for the creation of models to evaluate
        :param resultWriter: a writer with which to store results
        :param writePerDatasetResults: whether to use resultWriter (if not None) in order to generate detailed results for each
            dataset in a subdirectory named according to the name of the dataset
        :param crossValidatorParams: parameters to use for the instantiation of cross-validators
        :param columnNameForModelRanking: column name to use for ranking models
        :param rankMax: if true, use max for ranking, else min
        :return: a pair of data frames (allDF, meanDF) where allDF contains all the individual cross-validation results
            for every dataset and meanDF contains one row for each model with results averaged across datasets
        """
        allResults = pd.DataFrame()
        for key, inputOutputData in self.inputOutputDataDict.items():
            log.info(f"Evaluating models for {key}")
            models = [f() for f in modelFactories]
            modelsAreRegression = [model.isRegressionModel() for model in models]
            if all(modelsAreRegression):
                isRegression = True
            elif not any(modelsAreRegression):
                isRegression = False
            else:
                raise ValueError("The models have to be either all regression models or all classification, not a mixture")
            ev = createEvaluationUtil(inputOutputData, isRegression=isRegression, crossValidatorParams=crossValidatorParams)
            childResultWriter = resultWriter.childForSubdirectory(key) if writePerDatasetResults else None
            df = ev.compareModelsCrossValidation(models, resultWriter=childResultWriter)
            df[self.keyName] = key
            df["modelName"] = df.index
            if columnNameForModelRanking is not None:
                if columnNameForModelRanking not in df.columns:
                    raise ValueError(f"Rank metric {columnNameForModelRanking} not contained in columns {df.columns}")
                df["bestModel"] = 0
                if rankMax:
                    df["bestModel"].loc[df[columnNameForModelRanking].idxmax()] = 1
                else:
                    df["bestModel"].loc[df[columnNameForModelRanking].idxmin()] = 1
            df = df.reset_index(drop=True)
            allResults = pd.concat((allResults, df))
        strAllResults = f"All results:\n{allResults.to_string()}"
        log.info(strAllResults)
        meanResults = allResults.groupby("modelName").mean()
        strMeanResults = f"Mean results:\n{meanResults.to_string()}"
        log.info(strMeanResults)
        if resultWriter is not None:
            resultWriter.writeTextFile("model-comparison-results", strMeanResults + "\n\n" + strAllResults)
        return allResults, meanResults

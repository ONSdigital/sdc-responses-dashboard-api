import domready from "domready";
import pace from "pace-js";
import moment from "moment";

require("jquery-ui/ui/effect");
require("jquery-ui/ui/effects/effect-bounce");

const getReport = () => ({
  accountsPending: {
    id: "accounts-pending",
    title: "Accounts Pending",
    class: "fa fa-user-plus",
    tooltip: {
      placement: "bottom",
      title:
        "The number of accounts that have been created but not yet verified for this collection exercise."
    }
  },
  accountsEnrolled: {
    id: "accounts-enrolled",
    title: "Accounts Enrolled",
    class: "fa fa-users",
    tooltip: {
      placement: "bottom",
      title: "The number of verified accounts for this collection exercise."
    }
  },
  notStarted: {
    id: "not-started",
    title: "Not Started",
    class: "fa fa-times",
    tooltip: {
      placement: "bottom",
      title: `<strong>eQ</strong>: The number of cases where a questionnaire has not yet been launched. <p /><strong>SEFT</strong>: 
      The number of cases where a collection instrument has not been downloaded.`
    }
  },
  inProgress: {
    id: "in-progress",
    title: "In Progress",
    class: "fa fa-spinner",
    tooltip: {
      placement: "bottom",
      title: `<strong>eQ</strong>: The number of cases where a questionnaire has been launched. <p /><strong>SEFT</strong>: 
      The number of cases where a respondent has downloaded a collection instrument but not successfully uploaded the response.`
    }
  },
  completed: {
    id: "completed",
    title: "Completed",
    class: "fa fa-check",
    tooltip: {
      placement: "bottom",
      title: `<strong>eQ</strong>: The number of cases where a questionnaire has been successfully submitted and receipted. <p /><strong>SEFT</strong>: 
      The number of cases where a respondent has successfully uploaded a collection instrument.`
    }
  },
  sampleSize: {
    id: "sample-size",
    title: "Sample Size",
    class: "fa fa-sitemap fa-color-white",
    tooltip: {
      placement: "bottom",
      title:
        "The total number of cases for this collection exercise (excluding dummies sample units)."
    }
  }
});

const createCounters = (countersElement, figureData) => {
  const boxLayout = $("<div>", {
    class: "col-lg-6 col-sm-6 col-xs-12"
  });

  const innerBox = $("<div>", {
    class:
      figureData.name === "sampleSize"
        ? "small-box bg-ons-blue"
        : "small-box bg-ons-light-blue",
    id: `${figureData.id}-box`
  });

  const innerBoxText = $("<div>", {
    class: "inner"
  });

  const innerBoxTextChildOne = $("<h3>", {
    id: `${figureData.id}-counter`
  }).text(figureData.value);

  const innerBoxTextChildTwo = $("<p>").text(figureData.title);

  const innerBoxIcon = $("<div>", {
    class: "icon"
  });

  const innerBoxIconChildOne = $("<i>", {
    class: figureData.class
  });

  innerBoxIcon.append(innerBoxIconChildOne);
  innerBoxText.append([innerBoxTextChildOne, innerBoxTextChildTwo]);

  innerBox.append([innerBoxText, innerBoxIcon]);

  boxLayout.append(innerBox);
  countersElement.append(boxLayout);

  // Adds a minimal bounce animation to each counter
  $(`#${figureData.id}-counter`).effect("bounce", "slow");

  // Adds a tooltip to each counter
  $(`#${figureData.id}-box .inner`).tooltip({
    title: figureData.tooltip.title,
    placement: figureData.tooltip.placement,
    html: true
  });
};

const updateProgressData = response => {
  const timeUpdated = moment.unix(response.metadata.timeUpdated).calendar();

  $("#time-updated").text(timeUpdated);
  $("#progress-uploaded").text(response.report.completed);
  $("#progress-sample-size").text(response.report.sampleSize);

  const progress =
    (response.report.completed / response.report.sampleSize) * 100 || 0;
  const collexProgressBar = $("#collex-progress");
  collexProgressBar.css("width", `${progress}%`);

  if (progress >= 2) {
    collexProgressBar.text(`${progress.toFixed()}%`);
  } else {
    collexProgressBar.empty();
  }
};

const displayCollectionExerciseData = response => {
  const report = getReport();
  const countersElement = $("#counters");
  countersElement.empty();

  for (const figure in report) {
    if (report.hasOwnProperty(figure)) {
      const figureData = {
        name: figure,
        value: response.report[figure],
        id: report[figure].id,
        class: report[figure].class,
        title: report[figure].title,
        tooltip: {
          title: report[figure].tooltip.title,
          placement: report[figure].tooltip.placement
        }
      };

      // Creates a counter element for each figure
      createCounters(countersElement, figureData);
    }
  }

  updateProgressData(response);
};

const adjustWrapperMinHeight = () => {
  const windowHeight = $(window).height();
  const contentWrapper = $(".content-wrapper");
  const contentHeaderOuterHeight = $(".content-header").outerHeight();
  const mainContentOuterHeight = $("#main-content").outerHeight();
  const idealWrapperHeight = mainContentOuterHeight + contentHeaderOuterHeight;

  if (contentWrapper.height() != idealWrapperHeight) {
    contentWrapper.css("min-height", `${idealWrapperHeight}px`);
  }
  // 100 accounts for height of top-bar header and the footer
  if (idealWrapperHeight + 100 < windowHeight) {
    const diff = windowHeight - (idealWrapperHeight + 100);
    contentWrapper.css("min-height", `${idealWrapperHeight + diff}px`);
  }
};

const callAPI = () => {
  const collexBodyElement = $("#collex-id");
  const collexID = collexBodyElement.data("collex");
  const surveyID = collexBodyElement.data("survey");

  $.ajax({
    dataType: "json",
    url: `/dashboard/reporting/survey/${surveyID}/collection-exercise/${collexID}`
  })
    .done(result => {
      // Display content elements
      $(".content-header").show();
      $(".content").show();
      $("#time-updated-label").show();

      // Hide error content and loading animation
      $("#error-reporting").hide();
      $("#loading").hide();

      // Display the counters
      displayCollectionExerciseData(result);
    })
    .fail(() => {
      // Hide content elements
      $("#loading").hide();
      $(".content-header").hide();
      $(".content").hide();

      // Display error content
      $("#error-reporting").show();
    })
    .always(() => {
      // Refresh counter value if a valid refresh cycle is defined
      const reportingRefreshCycleInSeconds = collexBodyElement.data(
        "reporting-refresh-cycle"
      );
      const validReportingRefreshCycle =
        reportingRefreshCycleInSeconds >= 5 &&
        reportingRefreshCycleInSeconds <= 604800;

      if (validReportingRefreshCycle) {
        setTimeout(callAPI, reportingRefreshCycleInSeconds * 1000);
      }

      adjustWrapperMinHeight();
    });
};

domready(() => {
  // Invoke pace loading before AJAX event
  pace.start();
  callAPI();
});

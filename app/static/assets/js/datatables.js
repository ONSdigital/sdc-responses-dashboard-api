import domready from "domready";
import moment from "moment";
import $ from "jquery";

if (!window.$ || !window.jQuery) {
  window.$ = window.jQuery = $;
}

require("datatables.net")(window, $);
require("datatables.net-scroller")(window, $);
require("bootstrap/dist/js/bootstrap");

const setDataTableHeaderWidth = () => {
  // sets the width of the data table headers to 100%
  $(".dataTables_scrollHeadInner table").css("width", "100%");
};

const enableSearch = (searchElement, dataTable) => {
  searchElement.keyup(() => {
    dataTable.search(searchElement.val()).draw();
  });
};

const enableModalToggle = () => {
  const collexID = $("#collex-id").data("collex");

  if (!collexID) {
    $("#modal-survey").modal({
      backdrop: "static",
      keyboard: false
    });

    $("#modal-collex").attr({
      "data-backdrop": "static",
      "data-keyboard": "false"
    });
  }
};

const setCollexTableHeight = () => {
  // Dynamically set scroller rowHeight
  const checkCollexTableExist = setInterval(function() {
    const height = $("#collex-datatable tbody").height();
    if (height) {
      // sets the height of next div which follows the collex-datatable element
      $("#collex-datatable + div").height(height + 1);
      // sets the width of the headers to 100%
      setDataTableHeaderWidth();
      clearInterval(checkCollexTableExist);
    }
  }, 100);
};

const getCollectionExerciseGoLive = (collexIDs, eventTag) => {
  return $.ajax({
    dataType: "json",
    url: `/dashboard/collection-exercises/event/${eventTag}`,
    data: { collexIDs }
  });
};

const addCollectionExerciseData = (collexTable, surveys, surveyID) => {
  /**
   *  For each collex in the specified survey, the collex DataTable is updated with the collex data.
   */
  const collectionExercises = [];

  surveys.forEach(function(survey) {
    if (survey.surveyId === surveyID) {
      const collexIDs = [];
      const collectionExercisesCopy = [...survey.collectionExercises];

      collectionExercisesCopy.forEach(function(collex) {
        if (collex.userDescription === "") {
          collex.userDescription = "No description provided";
        }
        // collex.goLiveDate = "No go live provided";
        collexIDs.push(collex.collectionExerciseId);
        collectionExercises.push(collex);
      });

      const getCollectionExercisesWithGoLive = getCollectionExerciseGoLive(
        [...new Set(collexIDs)],
        "goLive"
      );

      getCollectionExercisesWithGoLive
        .done(result => {
          collectionExercisesCopy.forEach(function(collex) {
            collectionExercises.splice(collectionExercises.indexOf(collex), 1);
            collex.goLiveDate = result[collex.collectionExerciseId];
            collectionExercises.push(collex);
          });
        })
        .always(() => {
          collexTable.clear().draw();
          collexTable.rows.add(collectionExercises).draw();
        });
    }
  });
};

const customDateRenderer = (data, type, row, meta) => {
  if (type === "sort" || type === "type") {
    return data;
  } else if (moment(data, moment.ISO_8601, true).isValid()) {
    return moment(data).format("DD-MM-YYYY");
  } else {
    return "No go live provided";
  }
};

const initialiseSurveyDataTable = () =>
  $("#survey-datatable").DataTable({
    paging: true,
    lengthChange: false,
    searching: true,
    ordering: true,
    info: true,
    autoWidth: false,
    autoHeight: false,
    scrollY: "35vh",
    scrollCollapse: true,
    scroller: {
      loadingIndicator: false
    }
  });

const initialiseCollexDataTable = () =>
  $("#collex-datatable").DataTable({
    paging: true,
    lengthChange: false,
    searching: true,
    ordering: true,
    info: true,
    autoWidth: false,
    autoHeight: false,
    scrollY: "35vh",
    scrollCollapse: true,
    scroller: {
      loadingIndicator: false,
      rowHeight: 40
    },
    data: [],
    order: [[1, "desc"], [2, "desc"]],
    columns: [
      {
        data: "userDescription",
        defaultContent: "No description provided",
        title: "Collection Exercise Period",
        width: "50%"
      },
      {
        data: "goLiveDate",
        defaultContent: "No go live provided",
        title: "Go Live",
        width: "25%",
        render: customDateRenderer
      },
      {
        data: "scheduledReturnDateTime",
        defaultContent: "No return by date provided",
        title: "Return By Date",
        width: "25%",
        render: customDateRenderer
      }
    ],
    rowId: "collectionExerciseId"
  });

const populateCollexTable = (collexTable, surveyID) => {
  /*
   *  Load the collection exercise data into the data table
   */
  const surveys = JSON.parse($("#collex-id").data("surveys"));

  addCollectionExerciseData(collexTable, surveys, surveyID);

  $("#modal-collex").modal("toggle");

  // Dynamically set scroller rowHeight
  setCollexTableHeight();
};

const surveyTableClickEvent = (surveyTable, collexTable) =>
  $("#survey-datatable tbody").on("click", "tr", function() {
    const surveyID = surveyTable.row(this).id(); // eslint-disable-line no-invalid-this

    if (surveyID) {
      const surveyShortName = $(this).data("survey-short-name"); // eslint-disable-line no-invalid-this

      $("#chosen-survey").text(surveyShortName);
      $("#modal-survey").modal("toggle");

      populateCollexTable(collexTable, surveyID);
    }
  });

const collexTableClickEvent = collexTable =>
  $("#collex-datatable tbody").on("click", "tr", function() {
    const collexID = collexTable.row(this).id(); // eslint-disable-line no-invalid-this

    if (collexID) {
      const reportingPageCollexID = $("#collex-id").data("collex");

      if (!reportingPageCollexID) {
        window.location.href = `/dashboard/collection-exercise/${collexID}`;
      } else {
        window.location.href = collexID;
      }
    }
  });

const initialiseDataTables = () => {
  const surveyTable = initialiseSurveyDataTable();
  const collexTable = initialiseCollexDataTable();

  setDataTableHeaderWidth();

  enableSearch($("#survey-search"), surveyTable);
  enableSearch($("#collex-search"), collexTable);

  surveyTableClickEvent(surveyTable, collexTable);
  collexTableClickEvent(collexTable);
};

domready(() => {
  enableModalToggle();
  initialiseDataTables();
});

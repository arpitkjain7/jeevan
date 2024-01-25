import React, { useEffect, useState } from "react";
import {
  Page,
  Text,
  Document,
  StyleSheet,
  View,
  Font,
} from "@react-pdf/renderer";
import RedHatFont from "../../assets/fonts/Red_Hat_Display/static/RedHatDisplay-Regular.ttf";
import SourceSansFont from "../../assets/fonts/source-sans-pro/SourceSansPro-Regular.otf";
import SourceSansFontBold from "../../assets/fonts/source-sans-pro/SourceSansPro-Bold.otf";

Font.register({ family: "Red Hat Display", src: RedHatFont });
Font.register({ family: "Source Sans Pro", src: SourceSansFont });
Font.register({ family: "Source Sans Pro Bold", src: SourceSansFontBold });

const pmrPdfStyles = StyleSheet.create({
  document: {
    height: "100%",
    width: "100%",
  },
  pdfContainer: {
    padding: "8px 24px",
  },
  page: {
    backgroundColor: "#FFFFFF",
  },
  pdfHeader: {
    display: "flex",
    flexDirection: "row",
    flexDirection: "row",
    justifyContent: "space-between",
    backgroundColor: "#0089E9",
    borderBottom: "1px solid #ffffff",
    padding: "8px 16px",
  },
  pdfHeaderLogo: {
    display: "flex",
    flexDirection: "row",
    flexDirection: "row",
    gap: "16px",
  },
  pdflogoText: {
    color: "#ffffff",
    fontFamily: "Red Hat Display",
    fontSize: "16px",
    fontWeight: "400",
  },
  pdfhospitalNameText: {
    fontFamily: "Source Sans Pro",
    color: "#ffffff",
    fontSize: "16px",
    fontWeight: "400",
  },
  pdfDrNameText: {
    fontFamily: "Source Sans Pro",
    color: "#ffffff",
    fontSize: "16px",
    fontWeight: "400",
  },
  pdfPatientDetails: {
    backgroundColor: "#0089E9",
    borderBottom: "1px solid #ffffff",
    padding: "4px 16px",
  },
  pdfPatientNameText: {
    fontFamily: "Source Sans Pro Bold",
    color: "#ffffff",
    fontSize: "20px",
    fontWeight: "400",
  },
  pdfPatientName: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
  },
  pdfPatientOtherDetailsWrapper: {
    display: "flex",
    flexDirection: "row",
    flexWrap: "wrap",
    flexDirection: "row",
    padding: "4px 0px",
    backgroundColor: "#0089E9",
    gap: "6px",
  },
  pdfVitalsWrapper: {
    display: "flex",
    flexDirection: "row",
    flexWrap: "wrap",
    flexDirection: "row",
    padding: "12px 0px",
    gap: "6px",
    width: "100%",
  },
  pdfVital: {
    backgroundColor: "rgba(5, 97, 160, 0.08)",
    padding: "8px",
    minWidth: "24px",
    flex: 1,
  },
  pdfPatientOtherDetails: {
    backgroundColor: "rgba(255, 255, 255, 0.8)",
    padding: "4px",
    minWidth: "70px",
  },
  pdfPatientidText: {
    fontFamily: "Source Sans Pro Bold",
    color: "#ffffff",
    fontSize: "12px",
    fontWeight: "400",
  },
  dataLabel: {
    fontFamily: "Source Sans Pro",
    color: "#171717",
    fontSize: "10px",
    fontWeight: "400",
    textTransform: "capitalize",
  },
  dataValue: {
    fontFamily: "Source Sans Pro Bold",
    color: "#171717",
    fontSize: "12px",
    fontWeight: "400",
  },
  dataTitle: {
    fontFamily: "Source Sans Pro",
    color: "#5A5A5A",
    fontSize: "14px",
    fontWeight: "400",
    marginBottom: "8px",
  },
  table: {
    display: "table",
    width: "100%", // Take up full width
    borderStyle: "solid",
    borderWidth: 1,
    borderColor: "#000",
    paddingBottom: 5,
  },
  tableHeader: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "rgba(0, 137, 233, 0.2)",
  },
  tableRow: {
    flexDirection: "row",
    alignItems: "center",
    margin: "auto",
  },
  tableCell: {
    width: "25%", // Distribute columns evenly
    padding: 5,
    textAlign: "center",
    fontFamily: "Source Sans Pro Bold",
    color: "#171717",
    fontSize: "12px",
    fontWeight: "400",
  },
  rowCell: {
    width: "25%", // Distribute columns evenly
    padding: 5,
    textAlign: "center",
    fontFamily: "Source Sans Pro",
    color: "#171717",
    fontSize: "12px",
    fontWeight: "400",
  },
  rowText: {
    fontFamily: "Source Sans Pro",
    color: "#171717",
    fontSize: "12px",
    fontWeight: "400",
  },
  columnText: {
    fontFamily: "Source Sans Pro Bold",
    color: "#171717",
    fontSize: "12px",
    fontWeight: "400",
  },
  dataWrapper: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    gap: "8px",
    flexWrap: "wrap",
  },
  dataBox: {
    backgroundColor: "rgba(5, 97, 160, 0.08)",
    padding: "4px 6px",
    maxHeight: "50px",
    minWidth: "100px",
  },
  subDataContainer: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    gap: "2px",
  },
});

const PMRPdf = ({ patientData }) => {
  const [currentPatientData, setCurrentPatientData] = useState([]);
  // const [prescriptionData, setPrescriptionData] = useState([]);
  const pdfData = JSON.parse(sessionStorage.getItem("patientEMRDetails"));
  const columns = [
    { key: "medicine_name", label: "Medications" },
    { key: "frequency", label: "Frequency" },
    { key: "duration", label: "Duration" },
    { key: "dosage", label: "Dosage" },
  ];

  const transformPdfData = (inputObject) => {
    const resultArray = [];

    const sections = {
      vital: "Vitals",
      condition: "Conditions",
      examinationFindings: "Examination Findings",
      diagnosis: "Diagnosis",
      symptom: "Symptoms",
      medication: "Medications",
      currentMedication: "Current Medications",
      lab_investigation: "Lab Investigations",
      medical_history: "Medical History",
    };

    for (const section in sections) {
      if (
        inputObject[section] &&
        inputObject[section].data &&
        inputObject[section].data.length > 0
      ) {
        const heading = sections[section];
        let data = [];
        data = inputObject[section]?.data?.map((item) => {
          const labelData = Object.entries(item).map(([label, value]) => ({
            label,
            value,
          }));
          return labelData;
        });

        resultArray.push({ heading, data });
      }
    }

    return resultArray;
  };

  const [pmrPdfData, setPmrPdfData] = useState([]);

  useEffect(() => {
    if (Object.keys(patientData)?.length) {
      const patientDetails = [
        {
          label: "Gender",
          value: patientData?.patientGender,
        },
        {
          label: "Age",
          value: patientData?.patientAge,
        },
        {
          label: "Contact Number",
          value: patientData?.patientNumber,
        },
        {
          label: "Email",
          value: patientData?.patientEmail,
        },
      ];
      setCurrentPatientData(patientDetails);
    }
  }, []);

  return (
    <Document style={pmrPdfStyles.document}>
      <Page size="A4" style={pmrPdfStyles.page}>
        <View style={pmrPdfStyles.pdfHeader}>
          <View style={pmrPdfStyles.pdfHeaderLogo}>
            <Text style={pmrPdfStyles.pdflogoText}>Cliniq360</Text>
            <Text style={pmrPdfStyles.pdfhospitalNameText}>
              {patientData?.hospitalName}
            </Text>
          </View>
          <View style={pmrPdfStyles.drName}>
            <Text style={pmrPdfStyles.pdfDrNameText}>
              {patientData?.doctorName}
            </Text>
          </View>
        </View>
        <View style={pmrPdfStyles.pdfPatientDetails}>
          <View style={pmrPdfStyles.pdfPatientName}>
            <Text style={pmrPdfStyles.pdfPatientNameText}>
              {patientData?.patientName}
            </Text>
            <Text style={pmrPdfStyles.pdfPatientidText}>
              {patientData?.patientId}
            </Text>
          </View>
          <View style={pmrPdfStyles.pdfPatientOtherDetailsWrapper}>
            {currentPatientData?.map((item) => (
              <View style={pmrPdfStyles.pdfPatientOtherDetails}>
                <Text style={pmrPdfStyles.dataLabel}>{item.label}</Text>
                <Text style={pmrPdfStyles.dataValue}>{item?.value}</Text>
              </View>
            ))}
          </View>
        </View>
        <View style={pmrPdfStyles.pdfContainer}>
          {pdfData?.vital && (
            <View style={pmrPdfStyles?.dataContainer}>
              <Text style={pmrPdfStyles.dataTitle}>Vitals</Text>
              <View style={pmrPdfStyles?.dataWrapper}>
                {Object.entries(pdfData?.vital).map(([key, value]) =>
                  value ? (
                    <View style={pmrPdfStyles?.dataBox}>
                      <Text style={pmrPdfStyles?.dataLabel}>
                        {key.replace("_", " ")}
                      </Text>
                      <Text style={pmrPdfStyles?.dataValue}>{value}</Text>
                    </View>
                  ) : (
                    <></>
                  )
                )}
              </View>
            </View>
          )}
        </View>
        {pdfData?.medical_history?.data?.length ? (
          <View style={pmrPdfStyles.pdfContainer}>
            <View style={pmrPdfStyles?.dataContainer}>
              <Text style={pmrPdfStyles?.dataTitle}>Medical History</Text>
              <View style={pmrPdfStyles?.dataWrapper}>
                {pdfData?.medical_history?.data?.map(
                  (item) =>
                    item?.medical_history !== "[object Object]" && (
                      <View style={pmrPdfStyles?.dataBox}>
                        <Text style={pmrPdfStyles?.dataLabel}>
                          {item?.medical_history}
                        </Text>
                        <View style={pmrPdfStyles?.subDataContainer}>
                          <Text style={pmrPdfStyles?.dataValue}>
                            {item?.relationship}
                          </Text>
                        </View>
                      </View>
                    )
                )}
              </View>
            </View>
          </View>
        ) : (
          <View></View>
        )}
        {pdfData?.symptom?.data?.length ? (
          <View style={pmrPdfStyles.pdfContainer}>
            <View style={pmrPdfStyles.dataContainer}>
              <Text style={pmrPdfStyles.dataTitle}>Symptoms</Text>
              <View style={pmrPdfStyles.dataWrapper}>
                {pdfData.symptom?.data?.map((item) => (
                  <View style={pmrPdfStyles.dataBox}>
                    <Text style={pmrPdfStyles.dataLabel}>{item?.symptom}</Text>
                    <View style={pmrPdfStyles.subDataContainer}>
                      <Text style={pmrPdfStyles.dataValue}>
                        {item?.duration}
                      </Text>
                    </View>
                  </View>
                ))}
              </View>
            </View>
          </View>
        ) : (
          <View></View>
        )}
        {pdfData?.diagnosis?.data?.length ? (
          <View style={pmrPdfStyles.pdfContainer}>
            <View style={pmrPdfStyles.dataContainer}>
              <Text style={pmrPdfStyles.dataTitle}>Diagnosis</Text>
              <View style={pmrPdfStyles.dataWrapper}>
                {pdfData.diagnosis?.data?.map((item) => (
                  <View style={pmrPdfStyles.dataBox}>
                    <Text style={pmrPdfStyles.dataLabel}>{item?.disease}</Text>
                    <View style={pmrPdfStyles.subDataContainer}>
                      <Text style={pmrPdfStyles.dataValue}>
                        {item?.diagnosis_type}
                      </Text>
                      <Text style={pmrPdfStyles.dataValue}>|</Text>
                      <Text style={pmrPdfStyles.dataValue}>{item?.status}</Text>
                    </View>
                  </View>
                ))}
              </View>
            </View>
          </View>
        ) : (
          <View></View>
        )}
        {pdfData?.condition?.data?.length ? (
          <View style={pmrPdfStyles.pdfContainer}>
            <View style={pmrPdfStyles.dataContainer}>
              <Text style={pmrPdfStyles.dataTitle}>Condition</Text>
              <View style={pmrPdfStyles.dataWrapper}>
                {pdfData.condition?.data?.map((item) => (
                  <View style={pmrPdfStyles.dataBox}>
                    <Text style={pmrPdfStyles.dataLabel}>
                      {item?.condition}
                    </Text>
                    <View style={pmrPdfStyles.subDataContainer}>
                      <Text style={pmrPdfStyles.dataValue}>{item?.status}</Text>
                    </View>
                  </View>
                ))}
              </View>
            </View>
          </View>
        ) : (
          <View></View>
        )}
        {pdfData?.examination_findings?.data?.length ? (
          <View style={pmrPdfStyles.pdfContainer}>
            <View style={pmrPdfStyles.dataContainer}>
              <Text style={pmrPdfStyles.dataTitle}>Examination Findings</Text>
              <View style={pmrPdfStyles.dataWrapper}>
                {pdfData.examination_findings?.data?.map((item) => (
                  <View style={pmrPdfStyles.dataBox}>
                    <Text style={pmrPdfStyles.dataLabel}>{item?.disease}</Text>
                    <View style={pmrPdfStyles.subDataContainer}>
                      <Text style={pmrPdfStyles.dataValue}>{item?.notes}</Text>
                    </View>
                  </View>
                ))}
              </View>
            </View>
          </View>
        ) : (
          <View></View>
        )}
        {pdfData?.lab_investigation?.data?.length ? (
          <View style={pmrPdfStyles.pdfContainer}>
            <View style={pmrPdfStyles.dataContainer}>
              <Text style={pmrPdfStyles.dataTitle}>Lab Investigation</Text>
              <View style={pmrPdfStyles.dataWrapper}>
                {pdfData.lab_investigation?.data?.map((item) => (
                  <View style={pmrPdfStyles.dataBox}>
                    <Text style={pmrPdfStyles.dataLabel}>{item?.name}</Text>
                  </View>
                ))}
              </View>
            </View>
          </View>
        ) : (
          <View></View>
        )}
        <View style={pmrPdfStyles?.pdfContainer}>
          <Text style={pmrPdfStyles.dataTitle}>Prescription</Text>
          <View style={pmrPdfStyles.table}>
            <View style={pmrPdfStyles.tableHeader}>
              {columns.map((column) => (
                <Text style={pmrPdfStyles.tableCell} key={column.key}>
                  {column.label}
                </Text>
              ))}
            </View>
            {pdfData?.medication?.data?.map((item) => (
              <View style={pmrPdfStyles.tableRow} key={item.id}>
                {columns.map((column) => (
                  <Text style={pmrPdfStyles.rowCell} key={column.key}>
                    {item[column.key]}
                  </Text>
                ))}
              </View>
            ))}
          </View>
        </View>
        {pdfData?.notes ? (
          <View style={pmrPdfStyles.pdfContainer}>
            <View style={pmrPdfStyles?.dataContainer}>
              <Text style={pmrPdfStyles?.dataTitle}>Notes</Text>
              <View style={pmrPdfStyles?.dataWrapper}>
                <View style={pmrPdfStyles?.dataBox}>
                  <Text style={pmrPdfStyles?.dataLabel}>{pdfData?.notes}</Text>
                </View>
              </View>
            </View>
          </View>
        ) : (
          <View></View>
        )}
        {pdfData?.advice ? (
          <View style={pmrPdfStyles.pdfContainer}>
            <View style={pmrPdfStyles?.dataContainer}>
              <Text style={pmrPdfStyles?.dataTitle}>Advice</Text>
              <View style={pmrPdfStyles?.dataWrapper}>
                <View style={pmrPdfStyles?.dataBox}>
                  <Text style={pmrPdfStyles?.dataLabel}>{pdfData?.advice}</Text>
                </View>
              </View>
            </View>
          </View>
        ) : (
          <View></View>
        )}
      </Page>
    </Document>
  );
};

export default PMRPdf;

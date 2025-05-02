import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function EquipmentAnalysis() {
  // Dados originais
  const data = [
    { Seq: 1, V1: 375, V2: 135, V3: 458, V4: 475, V5: 509, V6: 336, V7: 469, V8: 492 },
    { Seq: 2, V1: 57, V2: 47, V3: 53, V4: 73, V5: 63, V6: 62, V7: 63, V8: 58 },
    { Seq: 3, V1: 245, V2: 267, V3: 242, V4: 227, V5: 271, V6: 219, V7: 268, V8: 286 },
    { Seq: 4, V1: 1472, V2: 1494, V3: 1462, V4: 1582, V5: 1613, V6: 1323, V7: 1490, V8: 1493 },
    { Seq: 5, V1: 105, V2: 66, V3: 103, V4: 103, V5: 118, V6: 98, V7: 101, V8: 118 },
    { Seq: 6, V1: 54, V2: 41, V3: 62, V4: 64, V5: 55, V6: 59, V7: 63, V8: 59 },
    { Seq: 7, V1: 193, V2: 209, V3: 184, V4: 235, V5: 207, V6: 172, V7: 223, V8: 156 },
    { Seq: 8, V1: 147, V2: 93, V3: 122, V4: 160, V5: 139, V6: 130, V7: 152, V8: 101 },
    { Seq: 9, V1: 1102, V2: 674, V3: 957, V4: 1137, V5: 1058, V6: 990, V7: 1098, V8: 878 },
    { Seq: 10, V1: 720, V2: 1033, V3: 566, V4: 874, V5: 628, V6: 646, V7: 706, V8: 320 },
    { Seq: 11, V1: 253, V2: 143, V3: 171, V4: 265, V5: 193, V6: 226, V7: 247, V8: 99 },
    { Seq: 12, V1: 685, V2: 586, V3: 750, V4: 803, V5: 830, V6: 615, V7: 699, V8: 777 },
    { Seq: 13, V1: 488, V2: 355, V3: 418, V4: 570, V5: 465, V6: 437, V7: 467, V8: 313 },
    { Seq: 14, V1: 198, V2: 187, V3: 220, V4: 203, V5: 247, V6: 176, V7: 209, V8: 204 },
    { Seq: 15, V1: 360, V2: 334, V3: 337, V4: 365, V5: 376, V6: 322, V7: 363, V8: 348 },
    { Seq: 16, V1: 1374, V2: 1506, V3: 1572, V4: 1256, V5: 1734, V6: 1235, V7: 1597, V8: 1684 },
    { Seq: 17, V1: 156, V2: 139, V3: 147, V4: 175, V5: 167, V6: 138, V7: 164, V8: 170 }
  ];

  const [analysisResults, setAnalysisResults] = useState(null);
  const [zScores, setZScores] = useState(null);
  const [deviationCounts, setDeviationCounts] = useState(null);

  useEffect(() => {
    // 1. Calcular médias e desvios padrão para cada sensor (linha)
    const sensorStats = data.map(row => {
      const values = [row.V1, row.V2, row.V3, row.V4, row.V5, row.V6, row.V7, row.V8];
      const mean = values.reduce((sum, val) => sum + val, 0) / values.length;
      const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
      const stdDev = Math.sqrt(variance);
      
      return {
        seq: row.Seq,
        mean,
        stdDev,
        values
      };
    });

    // 2. Calcular z-scores para cada valor (quanto se desvia da média)
    const zScoresByEquipment = {};
    for (let i = 1; i <= 8; i++) {
      const equipmentKey = `V${i}`;
      zScoresByEquipment[equipmentKey] = [];
    }

    sensorStats.forEach(stat => {
      stat.values.forEach((value, idx) => {
        const equipmentKey = `V${idx + 1}`;
        // Evitar divisão por zero
        const zScore = stat.stdDev > 0 ? (value - stat.mean) / stat.stdDev : 0;
        zScoresByEquipment[equipmentKey].push({
          sensorSeq: stat.seq,
          zScore,
          rawValue: value,
          mean: stat.mean,
          stdDev: stat.stdDev
        });
      });
    });

    // 3. Contar desvios significativos por equipamento
    const deviationThreshold = 2.0; // Z-score acima deste valor é considerado significativo
    const deviationCountsByEquipment = {};
    let totalDeviationsSum = 0;
    
    Object.keys(zScoresByEquipment).forEach(equipment => {
      const deviations = zScoresByEquipment[equipment].filter(item => 
        Math.abs(item.zScore) > deviationThreshold
      );
      
      const deviationSum = zScoresByEquipment[equipment].reduce((sum, item) => 
        sum + Math.abs(item.zScore), 0
      );
      
      deviationCountsByEquipment[equipment] = {
        count: deviations.length,
        sum: deviationSum,
        avgDeviation: deviationSum / zScoresByEquipment[equipment].length,
        details: deviations
      };
      
      totalDeviationsSum += deviationSum;
    });

    // 4. Calcular percentual de contribuição para desvios
    Object.keys(deviationCountsByEquipment).forEach(equipment => {
      deviationCountsByEquipment[equipment].percentageContribution = 
        (deviationCountsByEquipment[equipment].sum / totalDeviationsSum) * 100;
    });

    // 5. Calcular estatísticas por equipamento
    const equipmentStats = [];
    for (let i = 1; i <= 8; i++) {
      const equipmentKey = `V${i}`;
      const values = data.map(row => row[equipmentKey]);
      const sum = values.reduce((acc, val) => acc + val, 0);
      const mean = sum / values.length;
      const variance = values.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / values.length;
      const stdDev = Math.sqrt(variance);
      const cv = (stdDev / mean) * 100; // Coeficiente de variação

      equipmentStats.push({
        equipment: equipmentKey,
        sum,
        mean,
        stdDev,
        cv,
        deviations: deviationCountsByEquipment[equipmentKey]
      });
    }

    setAnalysisResults(equipmentStats);
    setZScores(zScoresByEquipment);
    setDeviationCounts(deviationCountsByEquipment);
  }, []);

  // Preparar dados para o gráfico de barras de desvios
  const prepareChartData = () => {
    if (!deviationCounts) return [];
    
    return Object.keys(deviationCounts).map(equipment => ({
      name: equipment,
      deviationCount: deviationCounts[equipment].count,
      avgDeviation: parseFloat(deviationCounts[equipment].avgDeviation.toFixed(2)),
      sumDeviation: parseFloat(deviationCounts[equipment].sum.toFixed(2)),
      percentageContribution: parseFloat(deviationCounts[equipment].percentageContribution.toFixed(2))
    }));
  };

  // Encontrar o equipamento mais provável de ser defeituoso
  const findDefectiveEquipment = () => {
    if (!analysisResults) return null;
    
    // Ordenar por percentual de contribuição de desvio (maior primeiro)
    const sorted = [...analysisResults].sort((a, b) => 
      b.deviations.percentageContribution - a.deviations.percentageContribution
    );
    
    return sorted[0];
  };

  const defectiveEquipment = findDefectiveEquipment();
  const chartData = prepareChartData();

  // Calcular média global para cada sensor e desvio percentual por equipamento
  const calculatePercentageDeviations = () => {
    if (!data) return [];
    
    const results = [];
    
    // Para cada sensor (linha)
    data.forEach(row => {
      const sensorId = row.Seq;
      const values = [row.V1, row.V2, row.V3, row.V4, row.V5, row.V6, row.V7, row.V8];
      const mean = values.reduce((sum, val) => sum + val, 0) / values.length;
      
      // Calcular desvio percentual para cada equipamento
      const deviations = values.map((value, idx) => ({
        equipment: `V${idx + 1}`,
        percentDeviation: ((value - mean) / mean) * 100
      }));
      
      // Ordenar por desvio absoluto (maior primeiro)
      const sortedDeviations = [...deviations].sort((a, b) => 
        Math.abs(b.percentDeviation) - Math.abs(a.percentDeviation)
      );
      
      results.push({
        sensorId,
        mean,
        deviations: sortedDeviations
      });
    });
    
    return results;
  };

  const percentageDeviations = calculatePercentageDeviations();

  // Contar quantas vezes cada equipamento tem o maior desvio percentual
  const countHighestDeviations = () => {
    if (!percentageDeviations || percentageDeviations.length === 0) return [];
    
    const counts = {};
    for (let i = 1; i <= 8; i++) {
      counts[`V${i}`] = 0;
    }
    
    percentageDeviations.forEach(sensor => {
      if (sensor.deviations && sensor.deviations.length > 0) {
        // Incrementar o contador para o equipamento com maior desvio absoluto
        const highestDeviation = sensor.deviations[0];
        counts[highestDeviation.equipment]++;
      }
    });
    
    return Object.keys(counts).map(equip => ({
      equipment: equip,
      count: counts[equip]
    })).sort((a, b) => b.count - a.count);
  };

  const highestDeviationCounts = countHighestDeviations();

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Análise de Equipamentos</h1>
      
      {defectiveEquipment && (
        <div className="bg-red-100 border border-red-400 text-red-700 p-4 mb-6 rounded">
          <h2 className="text-xl font-bold">Equipamento Defeituoso: {defectiveEquipment.equipment}</h2>
          <p className="mt-2">
            Este equipamento tem a maior contribuição para desvios totais ({defectiveEquipment.deviations.percentageContribution.toFixed(2)}%)
            com um desvio médio absoluto de {defectiveEquipment.deviations.avgDeviation.toFixed(3)}.
          </p>
        </div>
      )}

      <div className="mb-6">
        <h2 className="text-xl font-bold mb-2">Resumo das Análises</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white p-4 rounded shadow">
            <h3 className="font-bold mb-2">Desvios Percentuais</h3>
            <p>Equipamentos com o maior número de desvios extremos:</p>
            <ul className="list-disc pl-5 mt-2">
              {highestDeviationCounts.map((item, index) => (
                <li key={index} className={item.count > 4 ? "font-bold text-red-600" : ""}>
                  {item.equipment}: {item.count} sensores com maior desvio
                </li>
              ))}
            </ul>
          </div>
          
          <div className="bg-white p-4 rounded shadow">
            <h3 className="font-bold mb-2">Estatísticas dos Equipamentos</h3>
            <table className="min-w-full">
              <thead>
                <tr>
                  <th className="text-left">Equip.</th>
                  <th className="text-left">Média</th>
                  <th className="text-left">Desvio Pad.</th>
                  <th className="text-left">Coef. Var.</th>
                </tr>
              </thead>
              <tbody>
                {analysisResults && analysisResults.map((equip, index) => (
                  <tr key={index} className={equip === defectiveEquipment ? "bg-red-100" : ""}>
                    <td>{equip.equipment}</td>
                    <td>{equip.mean.toFixed(1)}</td>
                    <td>{equip.stdDev.toFixed(1)}</td>
                    <td>{equip.cv.toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-bold mb-4">Análise de Desvios por Equipamento</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="percentageContribution" name="Contribuição para Desvios (%)" fill="#8884d8" />
            <Bar dataKey="avgDeviation" name="Desvio Médio" fill="#82ca9d" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      
      <div className="mb-8">
        <h2 className="text-xl font-bold mb-2">Detalhes dos Desvios Significativos</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white">
            <thead>
              <tr>
                <th className="text-left p-2">Equipamento</th>
                <th className="text-left p-2">Sensores com Desvios Significativos</th>
              </tr>
            </thead>
            <tbody>
              {deviationCounts && Object.keys(deviationCounts).map((equipment, idx) => (
                <tr key={idx} className={equipment === (defectiveEquipment?.equipment || '') ? "bg-red-100" : ""}>
                  <td className="p-2 border">{equipment}</td>
                  <td className="p-2 border">
                    {deviationCounts[equipment].details.length > 0 ? (
                      <ul className="list-disc pl-5">
                        {deviationCounts[equipment].details.map((detail, i) => (
                          <li key={i}>
                            Sensor {detail.sensorSeq}: z-score = {detail.zScore.toFixed(2)} 
                            (valor: {detail.rawValue}, média: {detail.mean.toFixed(1)})
                          </li>
                        ))}
                      </ul>
                    ) : (
                      "Nenhum desvio significativo"
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      
      <div>
        <h2 className="text-xl font-bold mb-2">Conclusão</h2>
        <p className="bg-blue-50 p-4 rounded">
          Com base na análise dos dados, o equipamento <strong>{defectiveEquipment?.equipment}</strong> apresenta 
          o maior número de desvios significativos e a maior contribuição percentual para os desvios totais, 
          indicando que é o equipamento defeituoso entre os 8 analisados.
        </p>
      </div>
    </div>
  );
}

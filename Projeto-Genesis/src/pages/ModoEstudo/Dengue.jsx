import React, { useState } from 'react';
import './DengueCSS.css';

import homeIcon from '../../assets/HomeIconNav.png';
import calcIcon from '../../assets/CalculadoraIconNav.png';
import estudoIcon from '../../assets/EstudoIconNav.png';
import downloadBtn from '../../assets/DownloadBtn.png';
import visualizarBtn from '../../assets/VisualizarBtn.png';

const STEPS_TOTAL = 5;

const QUESTAO_2_GRUPOS = [
  { label: 'GRUPO A', correct: true },
  { label: 'GRUPO B', correct: false },
  { label: 'GRUPO C', correct: false },
  { label: 'GRUPO D', correct: false },
];

const QUESTAO_3_OPCOES = [
  { label: 'Febre alta persistente',        correct: false },
  { label: 'Exantema e cefaleia',            correct: false },
  { label: 'Choque ou disfunção grave de órgãos', correct: true },
  { label: 'Dor retro-orbitária isolada',   correct: false },
];

const TopBar = ({ step, total, onBack }) => (
  <div className="med-topbar">
    <button className="med-back-btn" onClick={onBack} aria-label="Voltar">
      ← Modo Estudo
    </button>
    <span className="med-step-badge">{step}/{total}</span>
  </div>
);

const BottomNav = () => (
  <nav className="bottom-nav" aria-label="Navegação principal">
    <button className="nav-btn" aria-label="Início">
      <img src={homeIcon} alt="Início" width="28" height="28" />
    </button>
    <button className="nav-btn" aria-label="Medicamentos">
      <img src={calcIcon} alt="Medicamentos" width="28" height="28" />
    </button>
    <button className="nav-btn" aria-label="Anotações">
      <img src={estudoIcon} alt="Anotações" width="28" height="28" />
    </button>
  </nav>
);

const Step1 = ({ onNext }) => (
  <div className="med-step">
    <h3 className="med-section-title">Caso Clínico</h3>

    <div className="med-card med-card--blue">
      <p>Paciente feminino, 26 anos, com febre há 2 dias, cefaleia, dor retro-orbitária, mialgia e artralgia. Nega comorbidades.</p>
    </div>

    <div className="med-card med-card--outline">
      <p>Temperatura: 38,5°</p>
      <p>PA: 110/70 mmHg</p>
      <p>FC: 88 bpm</p>
      <p className="med-mt-8">Sem sinais de alarmes</p>
    </div>

    <div className="med-card med-card--yellow">
      <p><strong>Objetivo:</strong> Aplicação do fluxograma da Dengue e definir a classificação, conduta e acompanhamento.</p>
    </div>

    <button className="med-btn med-btn--primary" onClick={onNext}>
      Iniciar o caso
    </button>
  </div>
);

const Step2 = ({ onNext }) => {
  const [sinalAlarme, setSinalAlarme]   = useState(null); 
  const [grupoSelecionado, setGrupo]    = useState(null); 
  const [erroSinal, setErroSinal]       = useState(false);
  const [erroGrupo, setErroGrupo]       = useState(false);
  const [tentativasGrupo, setTentativas] = useState(0);

  const handleSinal = (resposta) => {
    setSinalAlarme(resposta);
    setErroSinal(resposta === 'sim'); 
  };

  const handleGrupo = (index) => {
    const correto = QUESTAO_2_GRUPOS[index].correct;
    setGrupo(index);
    setErroGrupo(!correto);
    if (!correto) setTentativas(t => t + 1);
    if (correto) setTimeout(onNext, 600);
  };

  return (
    <div className="med-step">
      <p className="med-question">1. Há sinais de alarme ou gravidade?</p>

      <div className="med-card med-card--blue">
        <p className="med-small">Dor abdominal intensa e contínua, vômitos persistentes, acúmulo de líquidos, sangramento de mucosas, letargia/irritabilidade, hipotensão postural, hepatomegalia</p>
      </div>

      <div className="med-options">
        <button
          className={`med-btn ${
            sinalAlarme === 'sim'
              ? 'med-btn--error'
              : 'med-btn--outline'
          }`}
          onClick={() => handleSinal('sim')}
        >
          Sim
        </button>
        <button
          className={`med-btn ${
            sinalAlarme === 'nao'
              ? 'med-btn--success'
              : 'med-btn--outline'
          }`}
          onClick={() => handleSinal('nao')}
        >
          Não
        </button>
      </div>

      {erroSinal && (
        <p className="med-feedback med-feedback--error">
          Incorreto. A paciente não apresenta sinais de alarme descritos.
        </p>
      )}

      <p className="med-question med-mt-24">2. Com base nos achados clínicos, a qual grupo a paciente pertence?</p>

      <div className="med-options">
  {QUESTAO_2_GRUPOS.map((g, i) => {
    let variant = 'med-btn--outline';
    if (grupoSelecionado === i) {
      variant = g.correct ? 'med-btn--success' : 'med-btn--error';
    }
    return (
      <button
        key={g.label}
        className={`med-btn ${variant}`}
        onClick={() => handleGrupo(i)}
        disabled={
          sinalAlarme === null || 
          (grupoSelecionado !== null && QUESTAO_2_GRUPOS[grupoSelecionado].correct)
        }
      >
        {g.label}
      </button>
    );
  })}
</div>

      {erroGrupo && tentativasGrupo < 3 && (
        <p className="med-feedback med-feedback--error">
          Incorreto. Analise os critérios de classificação novamente.
        </p>
      )}
      {erroGrupo && tentativasGrupo >= 3 && (
        <p className="med-feedback med-feedback--hint">
          Dica: paciente sem sinais de alarme e sem sangramento → Grupo A.
        </p>
      )}
    </div>
  );
};

const Step3 = ({ onNext }) => (
  <div className="med-step">
    <p className="med-question">Classificação (Fluxograma)</p>

    <div className="med-card med-card--green med-card--center">
      <strong>DENGUE SEM SINAIS DE ALARME E SEM SANGRAMENTO (GRUPO A)</strong>
    </div>

    <p className="med-question med-mt-16">Conduta:</p>
    <div className="med-card med-card--outline">
      <ul className="med-list">
        <li>Hidratação oral</li>
        <li>Sintomáticos (dipirona ou paracetamol)</li>
        <li>Orientações sobre sinais de alarme</li>
        <li>Retorno diário até 48h após defervescência</li>
      </ul>
    </div>

    <div className="med-card med-card--yellow">
      <p><strong>Observação:</strong> Evitar AINEs e ácido acetilsalicílico. Manter hidratação adequada.</p>
    </div>

    <button className="med-btn med-btn--primary" onClick={onNext}>
      Continuar Com o Caso
    </button>

    <button className="med-btn med-btn--primary" onClick={onNext}>
      Voltar Para o Fluxograma
    </button>
  </div>
);

const Step4 = ({ onNext }) => {

  const [selecionado, setSelecionado] = useState(null);
  const [confirmado, setConfirmado] = useState(false);

  const handleSelect = (index) => {
    if (confirmado) return;
    
    if (selecionado === index) {
      setSelecionado(null);
    } else {
      setSelecionado(index);
    }
  };

  const handleConfirmar = () => {
    if (selecionado !== null) {
      setConfirmado(true);
    }
  };

  const getBotaoPrincipalProps = () => {
    if (!confirmado) {
      return {
        texto: 'Confirmar Resposta',
        acao: handleConfirmar,
        disabled: selecionado === null 
      };
    } else {
      const eCorreto = QUESTAO_3_OPCOES[selecionado].correct;
      return {
        texto: eCorreto ? 'Concluir' : 'Ver resposta correta',
        acao: onNext,
        disabled: false
      };
    }
  };

  const botaoProps = getBotaoPrincipalProps();

  return (
    <div className="med-step">
      <p className="med-question">3. Qual critério indica classificação imediata no Grupo D?</p>

      <div className="med-options med-mt-16">
        {QUESTAO_3_OPCOES.map((op, i) => {
          let variant = 'med-btn--outline';
          
          if (confirmado) {
            if (selecionado === i) {
              variant = op.correct ? 'med-btn--success' : 'med-btn--error';
            } else if (op.correct && !QUESTAO_3_OPCOES[selecionado].correct) {
            }
          } else {
            if (selecionado === i) {
              variant = 'med-btn--primary'; 
            }
          }

          return (
            <button
              key={op.label}
              className={`med-btn ${variant}`}
              onClick={() => handleSelect(i)}

              disabled={confirmado} 
            >
              {confirmado && op.correct && selecionado === i && <span className="med-check">✓ </span>}
              {op.label}
            </button>
          );
        })}
      </div>

      {confirmado && !QUESTAO_3_OPCOES[selecionado].correct && (
        <div className="med-card med-card--yellow med-mt-16">
          <p>O Grupo D <strong>representa dengue grave</strong> e exige atendimento emergencial imediato.</p>
        </div>
      )}

      {confirmado && QUESTAO_3_OPCOES[selecionado].correct && (
        <div className="med-mt-16">
          <p className="med-acerto">✓ Parabéns, você acertou!</p>
          <div className="med-card med-card--blue">
            <p className="med-small">
              A presença de choque, sangramento intenso ou comprometimento de órgãos como fígado, coração e sistema nervoso caracteriza risco elevado de morte, exigindo suporte intensivo imediato.
            </p>
          </div>
        </div>
      )}

      <button 
        className="med-btn med-btn--primary med-mt-16" 
        onClick={botaoProps.acao}
        disabled={botaoProps.disabled}
      >
        {botaoProps.texto}
      </button>
    </div>
  );
};

const Step5 = ({ onRestart, onNext }) => (
  <div className="med-step med-step--center">
    <div className="med-conclusao-icon">✓</div>
    <h3 className="med-conclusao-titulo">Protocolo concluído!</h3>
    <p className="med-conclusao-sub">Você completou o caso clínico de Dengue.</p>

    <div className="med-card med-card--outline med-mt-16">
      <p className="med-small"><strong>Resumo:</strong></p>
      <ul className="med-list med-small">
        <li>Sem sinais de alarme → Grupo A</li>
        <li>Tratamento ambulatorial com hidratação oral</li>
        <li>Evitar AINEs e AAS</li>
        <li>Retorno diário até 48h após defervescência</li>
      </ul>
    </div>

    <button className="med-btn med-btn--outline med-mt-16" onClick={onRestart}>
      Reiniciar caso
    </button>

    {/* Final do Caso */}
    <button className="med-btn med-btn--primary med-mt-16" onClick={onNext}>
      Voltar Para o Fluxograma
    </button>
  </div>
);

const ModoEstudoDengue = () => {
  const [step, setStep] = useState(1);

  const next    = () => setStep(s => Math.min(s + 1, STEPS_TOTAL));
  const back    = () => setStep(s => Math.max(s - 1, 1));
  const restart = () => setStep(1);

  const renderStep = () => {
    switch (step) {
      case 1: return <Step1 onNext={next} />;
      case 2: return <Step2 onNext={next} />;
      case 3: return <Step3 onNext={next} />;
      case 4: return <Step4 onNext={next} />;
      case 5: return <Step5 onRestart={restart} />;
      default: return null;
    }
  };

  return (
    <div className="med-page-wrapper">
      <div className="med-mobile-frame">
        <TopBar step={step} total={STEPS_TOTAL} onBack={back} />
        
        <div className="med-content">
          {renderStep()}
        </div>

        {/* Botões Flutuantes (Visualizar / Download) */}
        <div className="fab-group">
          <button className="fab-btn" aria-label="Baixar">
            <img src={downloadBtn} alt="Baixar" width="36" height="36" />
          </button>
          <button className="fab-btn" aria-label="Visualizar">
            <img src={visualizarBtn} alt="Visualizar" width="36" height="36" />
          </button>
        </div>

        <BottomNav />
      </div>
    </div>
  );
};

export default ModoEstudoDengue;